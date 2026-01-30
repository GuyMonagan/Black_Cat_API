from celery import shared_task

@shared_task
def test_hello():
    print("🐍 Task worked! Hello from Celery!")
