from django.db import models
from django.utils import timezone

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    """
    Модель заимствования книги пользователем.

    Поля:
    - user: Пользователь, который берёт книгу.
    - book: Книга, которую берут.
    - borrow_date: Дата заимствования (по умолчанию — текущая).
    - return_date: Дата возврата книги. Может быть пустой, если книга ещё не возвращена.
    - is_returned: Булево значение, указывающее, возвращена ли книга.

    Методы:
    - __str__: Возвращает строковое представление заимствования в формате "username → book title".
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrow_date = models.DateField(default=timezone.now)
    expected_return_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"
