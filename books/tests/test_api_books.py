import pytest
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse
from books.models import Book, Author, Genre, Location


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


@pytest.mark.parametrize("user_role, expected_status", [
    ("reader", 403),
    ("librarian", 201),
])
@pytest.mark.django_db
def test_book_creation_permissions_by_role(user_role, expected_status):
    client = APIClient()
    user = User.objects.create_user(
        email=f"{user_role}@example.com",
        password="testpass",
        role=user_role
    )
    client.force_authenticate(user=user)

    author = Author.objects.create(name="Автор")
    genre = Genre.objects.create(name="Фантастика")

    data = {
        "title": "Тестовая книга",
        "author": author.id,
        "genre": genre.id,
        "total_count": 3,
        "available_count": 3
    }
    response = client.post(reverse("book-list"), data)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_anonymous_user_cannot_create_book():
    client = APIClient()

    author = Author.objects.create(name="Автор")
    genre = Genre.objects.create(name="Фантастика")

    data = {
        "title": "Безымянная книга",
        "author": author.id,
        "genre": genre.id,
        "total_count": 3,
        "available_count": 3
    }

    response = client.post(reverse("book-list"), data)
    assert response.status_code == 401


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def book_data(db):
    author = Author.objects.create(name="Лев Толстой")
    genre = Genre.objects.create(name="Роман")
    location = Location.objects.create(address="Зал 1", shelf_code="A1")

    books = []
    for i in range(1, 7):
        books.append(Book.objects.create(
            title=f"Книга {i}",
            description="Описание книги",
            author=author,
            genre=genre,
            location=location,
            total_count=5,
            available_count=5,
            publication_year=2000 + i
        ))
    return books


def test_book_list_pagination(api_client, book_data):
    url = reverse("book-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 5  # пагинация: PAGE_SIZE = 5
    assert response.data["count"] == 6


def test_book_search(api_client, book_data):
    url = reverse("book-list")
    response = api_client.get(url, {"search": "Книга 6"})

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Книга 6"


def test_book_ordering(api_client, book_data):
    url = reverse("book-list")
    response = api_client.get(url, {"ordering": "-publication_year"})

    assert response.status_code == 200
    years = [book["publication_year"] for book in response.data["results"]]
    assert years == sorted(years, reverse=True)[:5]


def test_book_filter(api_client, book_data):
    genre_id = book_data[0].genre.id
    url = reverse("book-list")
    response = api_client.get(url, {"genre": genre_id})

    assert response.status_code == 200
    assert all(book["genre"]["id"] == genre_id for book in response.data["results"])


@pytest.mark.django_db
def test_cannot_create_book_without_title(api_client):
    user = User.objects.create_user(
        email="lib@example.com",
        password="testpass",
        role="librarian"
    )
    api_client.force_authenticate(user=user)

    author = Author.objects.create(name="Автор")

    data = {
        "author": author.id,
        "total_count": 3,
        "available_count": 3,
    }

    response = api_client.post(reverse("book-list"), data)

    assert response.status_code == 400
    assert "title" in response.data


@pytest.mark.django_db
def test_book_list_returns_nested_author(api_client, book_data):
    response = api_client.get(reverse("book-list"))

    book = response.data["results"][0]

    assert isinstance(book["author"], dict)
    assert "name" in book["author"]


@pytest.mark.django_db
def test_available_count_cannot_exceed_total(api_client):
    user = User.objects.create_user(
        email="lib@example.com",
        password="testpass",
        role="librarian"
    )
    api_client.force_authenticate(user=user)

    author = Author.objects.create(name="Автор")

    data = {
        "title": "Ломаная книга",
        "author": author.id,
        "total_count": 2,
        "available_count": 5,
    }

    response = api_client.post(reverse("book-list"), data)

    assert response.status_code == 400
