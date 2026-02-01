import requests
from django.conf import settings
from users.models import TelegramToken


def connect(update, context):
    """
    Обрабатывает команду /connect от пользователя Telegram.
    Привязывает Telegram-аккаунт к пользователю по одноразовому токену.
    """
    try:
        token = context.args[0]
    except IndexError:
        update.message.reply_text("⚠️ Укажи токен: /connect <токен>")
        return

    try:
        token_obj = TelegramToken.objects.get(token=token)
        user = token_obj.user
        user.telegram_chat_id = update.effective_chat.id
        user.save()
        token_obj.delete()  # Удаляем токен после использования
        update.message.reply_text("✅ Telegram успешно привязан к вашему аккаунту!")
    except TelegramToken.DoesNotExist:
        update.message.reply_text("❌ Токен недействителен или устарел.")


def send_telegram_message(chat_id: str, message: str) -> bool:
    """
    Отправляет сообщение в Telegram-пользователю через Bot API.
    Возвращает True при успехе, иначе False.
    """
    if not chat_id:
        return False

    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        print(f"DEBUG: Status {response.status_code}, Response: {response.text}")
        return response.status_code == 200
    except requests.RequestException:
        return False
