from django.apps import AppConfig


class BooksConfig(AppConfig):
    """
    Конфигурация приложения 'books'.
    Используется Django для регистрации и настройки приложения книг.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
