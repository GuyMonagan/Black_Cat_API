from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Конфигурация приложения 'reports'.
    Используется для генерации отчётов без собственной модели.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"
