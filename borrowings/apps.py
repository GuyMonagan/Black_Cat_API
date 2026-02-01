from django.apps import AppConfig


class BorrowingsConfig(AppConfig):
    """
    Конфигурация приложения 'borrowings'.
    Определяет базовые настройки для работы с арендой книг.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowings"
