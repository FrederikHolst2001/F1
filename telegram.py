import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_alert(msg):

    if "PASTE" in TELEGRAM_TOKEN:
        return

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )