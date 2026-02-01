import pytest
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from users.models import User
from books.models import Book, Author, Genre
from borrowings.models import Borrowing


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_data():
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    author = Author.objects.create(name="Толстой")
    genre = Genre.objects.create(name="Роман")

    book1 = Book.objects.create(title="Анна Каренина", author=author, genre=genre)
    book2 = Book.objects.create(title="Война и мир", author=author, genre=genre)

    return user, book1, book2

@pytest.mark.django_db
def test_popular_books(api_client, sample_data):
    user, book1, book2 = sample_data

    Borrowing.objects.create(user=user, book=book1)
    Borrowing.objects.create(user=user, book=book1)
    Borrowing.objects.create(user=user, book=book2)

    response = api_client.get("/api/reports/popular_books/")
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert response.data[0]["title"] == "Анна Каренина"
    assert response.data[0]["times_borrowed"] == 2

@pytest.mark.django_db
def test_debtors_list(api_client, sample_data):
    user, book1, _ = sample_data
    yesterday = timezone.now().date() - timedelta(days=1)

    Borrowing.objects.create(
        user=user,
        book=book1,
        borrow_date=yesterday,
        return_date=None,
        is_returned=False,
        expected_return_date=yesterday,
    )

    response = api_client.get("/api/reports/debtors/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["user"] == user.email
    assert response.data[0]["book"] == "Анна Каренина"

@pytest.mark.django_db
def test_lost_books(api_client, sample_data):
    user, book1, _ = sample_data
    overdue = timezone.now().date() - timedelta(days=31)

    Borrowing.objects.create(
        user=user,
        book=book1,
        borrow_date=overdue,
        return_date=None,
        is_returned=False,
        expected_return_date=overdue,
    )

    response = api_client.get("/api/reports/lost_books/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["book"] == "Анна Каренина"
