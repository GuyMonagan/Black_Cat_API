import pytest
from rest_framework.test import APIClient
from users.models import User
from books.models import Book, Author, Genre
from borrowings.models import Borrowing


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_reader_can_create_borrowing(api_client):
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=user)

    author = Author.objects.create(name="Толстой")
    genre = Genre.objects.create(name="Роман")
    book = Book.objects.create(title="Анна Каренина", author=author, genre=genre, total_count=3, available_count=2)

    data = {
        "book": book.id,
        "borrow_date": "2024-01-01",
        "expected_return_date": "2024-01-20"
    }

    response = api_client.post("/api/borrowings/", data)

    assert response.status_code == 201
    assert response.data["book"] == book.id
    assert Borrowing.objects.filter(user=user, book=book).exists()


@pytest.mark.django_db
def test_anonymous_cannot_create_borrowing(api_client):
    response = api_client.post("/api/borrowings/", {})
    assert response.status_code == 401


@pytest.mark.django_db
def test_reader_cannot_update_or_delete(api_client):
    reader = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=reader)

    author = Author.objects.create(name="Булгаков")
    genre = Genre.objects.create(name="Фантастика")
    book = Book.objects.create(title="Мастер и Маргарита", author=author, genre=genre, total_count=2, available_count=1)

    borrowing = Borrowing.objects.create(user=reader, book=book)

    update_data = {"return_date": "2024-12-31"}

    response = api_client.patch(f"/api/borrowings/{borrowing.id}/", update_data)
    assert response.status_code == 403

    response = api_client.delete(f"/api/borrowings/{borrowing.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_reader_sees_only_own_borrowings(api_client):
    reader = User.objects.create_user(email="reader1@lib.com", password="123", role="reader")
    other_reader = User.objects.create_user(email="reader2@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=reader)

    author = Author.objects.create(name="Достоевский")
    genre = Genre.objects.create(name="Триллер")
    book = Book.objects.create(title="Идиот", author=author, genre=genre)

    Borrowing.objects.create(user=reader, book=book)
    Borrowing.objects.create(user=other_reader, book=book)

    response = api_client.get("/api/borrowings/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["user"]["email"] == reader.email


@pytest.mark.django_db
def test_admin_sees_all_borrowings(api_client):
    admin = User.objects.create_user(email="admin@lib.com", password="123", role="admin")
    api_client.force_authenticate(user=admin)

    author = Author.objects.create(name="Гоголь")
    genre = Genre.objects.create(name="Мистика")
    book = Book.objects.create(title="Вий", author=author, genre=genre)

    user1 = User.objects.create_user(email="user1@lib.com", password="123", role="reader")
    user2 = User.objects.create_user(email="user2@lib.com", password="123", role="reader")

    Borrowing.objects.create(user=user1, book=book)
    Borrowing.objects.create(user=user2, book=book)

    response = api_client.get("/api/borrowings/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
