import pytest
from rest_framework.test import APIClient
from users.models import User
from books.models import Book, Author, Genre
from reviews.models import Review


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def book():
    author = Author.objects.create(name="Толстой")
    genre = Genre.objects.create(name="Роман")
    return Book.objects.create(title="Война и мир", author=author, genre=genre)


@pytest.mark.django_db
def test_reader_can_create_review(api_client, book):
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=user)

    data = {
        "book": book.id,
        "text": "Отличная книга!",
        "rating": 5
    }

    response = api_client.post("/api/reviews/", data)
    assert response.status_code == 201
    assert Review.objects.filter(book=book, user=user).exists()


@pytest.mark.django_db
def test_reader_cannot_see_unapproved_reviews(api_client, book):
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    other = User.objects.create_user(email="another@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=user)

    Review.objects.create(book=book, user=other, text="Скрытый отзыв", rating=3, is_approved=False)

    response = api_client.get("/api/reviews/")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_admin_sees_all_reviews(api_client, book):
    admin = User.objects.create_user(email="admin@lib.com", password="123", role="admin")
    user = User.objects.create_user(email="user@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=admin)

    Review.objects.create(book=book, user=user, text="Показать админу", rating=4, is_approved=False)

    response = api_client.get("/api/reviews/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_owner_can_update_review(api_client, book):
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=user)

    review = Review.objects.create(book=book, user=user, text="Старый текст", rating=3, is_approved=True)

    data = {"text": "Обновлён", "rating": 4, "book": book.id}
    response = api_client.patch(f"/api/reviews/{review.id}/", data)
    assert response.status_code == 200
    review.refresh_from_db()
    assert review.text == "Обновлён"
    assert review.rating == 4


@pytest.mark.django_db
def test_librarian_can_approve_review(api_client, book):
    librarian = User.objects.create_user(email="lib@lib.com", password="123", role="librarian")
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=librarian)

    review = Review.objects.create(book=book, user=user, text="Нужна проверка", rating=4)

    response = api_client.post(f"/api/reviews/{review.id}/approve/")
    assert response.status_code == 200
    review.refresh_from_db()
    assert review.is_approved is True


@pytest.mark.django_db
def test_others_cannot_approve_review(api_client, book):
    user = User.objects.create_user(email="reader@lib.com", password="123", role="reader")
    other_user = User.objects.create_user(email="user2@lib.com", password="123", role="reader")
    api_client.force_authenticate(user=user)

    review = Review.objects.create(book=book, user=other_user, text="Кто ты такой?", rating=1)

    response = api_client.post(f"/api/reviews/{review.id}/approve/")
    assert response.status_code == 403
    review.refresh_from_db()
    assert review.is_approved is False
