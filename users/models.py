from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    """
    Перечисление ролей пользователей в системе.

    Значения:
    - READER: Обычный пользователь, который может только читать и брать книги.
    - LIBRARIAN: Библиотекарь, управляет книгами и выдачей.
    - ADMIN: Администратор системы, имеет полный доступ.
    """
    READER = 'reader', 'Reader'
    LIBRARIAN = 'librarian', 'Librarian'
    ADMIN = 'admin', 'Admin'

class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартного пользователя Django.

    Добавленные поля:
    - role: Роль пользователя в системе. По умолчанию — читатель.

    Методы:
    - __str__: Возвращает строковое представление пользователя в формате "username (роль)".
    """
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
