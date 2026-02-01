from celery import shared_task
from datetime import date, timedelta
from borrowings.models import Borrowing
from core.telegram_bot import send_telegram_message

@shared_task
def send_due_soon_reminders():
    """
    Отправляет напоминания пользователям, у которых завтра истекает срок аренды книги.
    """
    tomorrow = date.today() + timedelta(days=1)
    borrowings = Borrowing.objects.filter(expected_return_date=tomorrow, is_returned=False)

    for borrowing in borrowings:
        user = borrowing.user
        if user.telegram_chat_id:
            message = (
                f"📚 Напоминание!\n"
                f"Завтра нужно вернуть книгу: «{borrowing.book.title}».\n"
                f"Не забудь её отнести в библиотеку 👀"
            )
            send_telegram_message(user.telegram_chat_id, message)
