from django.core.management.base import BaseCommand
from django.conf import settings

from telegram.ext import Updater, CommandHandler

from core.telegram_bot import connect


class Command(BaseCommand):
    """
    Команда для запуска Telegram-бота через Django manage.py.
    Используется как: python manage.py startbot
    """
    help = "Запускает Telegram-бота"

    def handle(self, *args, **options):
        updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("connect", connect))

        self.stdout.write(self.style.SUCCESS("🤖 Telegram Bot is running..."))
        updater.start_polling()
        updater.idle()
