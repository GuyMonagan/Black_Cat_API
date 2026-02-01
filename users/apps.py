from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения 'users'.
    Отвечает за регистрацию, аутентификацию и профиль пользователей.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
