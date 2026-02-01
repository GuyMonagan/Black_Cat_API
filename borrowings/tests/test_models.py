import pytest
from django.utils import timezone
from users.models import User
from books.models import Book, Author, Genre
from borrowings.models import Borrowing
from django.utils import timezone


@pytest.mark.django_db
def test_borrowing_str():
    """
    Проверяет, что метод __str__() у Borrowing возвращает корректную строку.
    """
    user = User.objects.create_user(email="user@example.com", password="123", role="reader")
    author = Author.objects.create(name="Гоголь")
    genre = Genre.objects.create(name="Ужасы")
    book = Book.objects.create(title="Вий", author=author, genre=genre, total_count=1, available_count=1)

    borrowing = Borrowing.objects.create(user=user, book=book)

    assert str(borrowing) == f"{user.username} → {book.title}"


@pytest.mark.django_db
def test_borrowing_defaults():
    """
    Проверяет значения по умолчанию для аренды (is_returned, borrow_date).
    """
    user = User.objects.create_user(email="user@example.com", password="123", role="reader")
    author = Author.objects.create(name="Пушкин")
    genre = Genre.objects.create(name="Поэзия")
    book = Book.objects.create(title="Руслан и Людмила", author=author, genre=genre)

    borrowing = Borrowing.objects.create(user=user, book=book)
    borrowing.refresh_from_db()

    assert borrowing.is_returned is False
    assert borrowing.borrow_date == timezone.localdate()
