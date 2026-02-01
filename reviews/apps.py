from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Конфигурация приложения 'reviews'.
    Обрабатывает пользовательские отзывы на книги.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
