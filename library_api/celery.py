import os

from celery import Celery

# Устанавливаем Django settings по умолчанию для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_api.settings")

# Создаём экземпляр Celery-приложения
app = Celery("library_api")

# Загружаем конфигурацию из Django settings
# Все настройки должны начинаться с префикса CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находит tasks.py во всех INSTALLED_APPS
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Тестовая Celery-задача для проверки корректной работы воркера.
    """
    print(f"🔧 [Celery Debug] Task executed: {self.request!r}")
