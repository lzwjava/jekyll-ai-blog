import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "610574272")

TELEGRAM_MAX_LENGTH = 4096


def send_telegram_message(message):
    """Send a message to Telegram, handling long messages by splitting them."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_API_KEY or TELEGRAM_CHAT_ID not set.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    url_pattern = re.compile(r"(https?://[^\s]+)")
    message_no_stars = message.replace("*", "")
    message_no_links = url_pattern.sub("", message_no_stars)

    messages = []
    msg = message_no_links
    while len(msg) > TELEGRAM_MAX_LENGTH:
        split_idx = msg.rfind("\n", 0, TELEGRAM_MAX_LENGTH)
        if split_idx == -1 or split_idx < TELEGRAM_MAX_LENGTH // 2:
            split_idx = TELEGRAM_MAX_LENGTH
        messages.append(msg[:split_idx])
        msg = msg[split_idx:]
    messages.append(msg)

    success = True
    for part in messages:
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": part,
        }
        try:
            response = requests.post(url, params=params, timeout=30)
            response.raise_for_status()
            print(f"Successfully sent Telegram message part ({len(part)} chars).")
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            success = False

    return success
