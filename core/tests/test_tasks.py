from datetime import date, timedelta
from unittest.mock import patch

import pytest

from books.models import Author, Book, Genre
from borrowings.models import Borrowing
from core.tasks import send_due_soon_reminders
from users.models import User


@pytest.mark.django_db
@patch("core.tasks.send_telegram_message")
def test_send_due_soon_reminders_sends_messages(mock_send):
    """
    Проверяет, что таска отправляет напоминания пользователям,
    если дата возврата книги — завтра.
    """
    user = User.objects.create_user(
        email="reader@lib.com",
        password="123",
        role="reader",
        telegram_chat_id="987654321",
    )

    author = Author.objects.create(name="Булгаков")
    genre = Genre.objects.create(name="Роман")
    book = Book.objects.create(
        title="Мастер и Маргарита",
        author=author,
        genre=genre,
        total_count=5,
        available_count=2,
    )

    # Создаём аренду с возвратом на завтра
    Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date.today(),
        expected_return_date=date.today() + timedelta(days=1),
        is_returned=False,
    )

    send_due_soon_reminders()

    mock_send.assert_called_once_with(
        "987654321",
        "📚 Напоминание!\nЗавтра нужно вернуть книгу: «Мастер и Маргарита».\nНе забудь её отнести в библиотеку 👀",
    )
