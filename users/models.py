from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей для модели User.

    Методы:
        create_user(email, password, **extra_fields): Создаёт обычного пользователя.
        create_superuser(email, password, **extra_fields): Создаёт суперпользователя с правами администратора.
    """
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



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
    Кастомная модель пользователя, основанная на AbstractUser,
    с удалённым полем username и авторизацией по email.

    Поля:
        email (EmailField): Уникальный адрес электронной почты, используемый как логин.
        telegram_chat_id (CharField): Необязательный ID для связи с Telegram.
        role (CharField): Роль пользователя в системе (reader, librarian, admin).

    Атрибуты:
        USERNAME_FIELD (str): Указывает, что email используется как уникальный идентификатор.
        REQUIRED_FIELDS (list): Список дополнительных обязательных полей при создании суперпользователя (пустой).

    Методы:
        __str__(): Возвращает строковое представление пользователя в виде "email (роль)".
    """
    username = None  # удаляем username
    email = models.EmailField(unique=True)  # делаем email уникальным

    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )

    USERNAME_FIELD = 'email'  # теперь логин по email
    REQUIRED_FIELDS = []  

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
