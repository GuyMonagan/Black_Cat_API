from unittest.mock import patch
import pytest
from users.models import User
from books.models import Book, Author, Genre
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@patch("core.telegram_bot.send_telegram_message")
def test_telegram_sent_on_borrowing(mock_send, api_client):
    """
    Проверяет, что при создании аренды с chat_id вызывается отправка сообщения в Telegram.
    """
    user = User.objects.create_user(
        email="reader@lib.com",
        password="123",
        role="reader",
        telegram_chat_id="123456789"
    )
    api_client.force_authenticate(user=user)

    author = Author.objects.create(name="Толстой")
    genre = Genre.objects.create(name="Роман")
    book = Book.objects.create(title="Анна Каренина", author=author, genre=genre, total_count=3, available_count=3)

    data = {
        "book": book.id,
        "borrow_date": "2024-01-01",
        "expected_return_date": "2024-01-20"
    }

    response = api_client.post("/api/borrowings/", data)
    assert response.status_code == 201
    assert mock_send.called
