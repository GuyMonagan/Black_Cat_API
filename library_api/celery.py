import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_api.settings')

app = Celery('library_api')

# Загружаем конфиг из settings.py, CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит таски в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'🔧 [Celery Debug] Task executed: {self.request!r}')
