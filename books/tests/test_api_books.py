import pytest
from rest_framework.test import APIClient
from books.models import Book
import pytest
from rest_framework.test import APIClient
from users.models import User
from books.models import Author, Genre


@pytest.mark.django_db
def test_book_list_returns_books():
    client = APIClient()

    response = client.get("/api/books/")

    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert all("title" in book for book in response.data['results'])


@pytest.mark.django_db
def test_librarian_can_create_book():
    user = User.objects.create_user(
        email="lib@example.com", password="testpass", role="librarian"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    author = Author.objects.create(name="Test Author")
    genre = Genre.objects.create(name="Fantasy")

    data = {
        "title": "New Book",
        "description": "A test book.",
        "author": author.id,
        "genre": genre.id,
        "total_count": 5,
        "available_count": 5,
    }

    response = client.post("/api/books/", data)

    assert response.status_code == 201
    assert response.data["title"] == "New Book"


@pytest.mark.django_db
def test_reader_cannot_create_book():
    user = User.objects.create_user(
        email="reader@example.com", password="testpass", role="reader"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/books/", {})

    assert response.status_code == 403  # Forbidden
