from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Конфигурация приложения core.

    Используется Django для регистрации приложения, задания имени
    и определения типа primary key по умолчанию.

    В данном приложении core хранится инфраструктурная логика:
    - Celery-задачи
    - интеграция с Telegram
    - вспомогательные сервисы, не связанные напрямую с API
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
