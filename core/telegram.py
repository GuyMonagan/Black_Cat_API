import requests
from django.conf import settings

def send_telegram_message(chat_id: str, message: str) -> bool:
    """
    Отправляет сообщение в Telegram-пользователю через Bot API.
    Возвращает True, если успешно, False иначе.
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
