import os
import requests
from dotenv import load_dotenv
import json
import subprocess
import argparse

load_dotenv()

TELEGRAM_BOT_API_KEY = os.environ.get("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHAT_ID = "-4714712674"


def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(
            f"Error sending Telegram message: {response.status_code} - {response.text}"
        )


def _get_chat_id(bot_token):
    """Retrieves the chat ID of the last message sent to the bot.

    NOTE: This uses getUpdates which conflicts with OpenClaw's Telegram polling.
    Only use this as a standalone script, not while OpenClaw is running.
    Kept here for reference only.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        updates = response.json()
        print(json.dumps(updates, indent=4))
        if updates["result"]:
            last_update = updates["result"][-1]
            if "message" in last_update and "chat" in last_update["message"]:
                return last_update["message"]["chat"]["id"]
            elif (
                "edited_message" in last_update
                and "chat" in last_update["edited_message"]
            ):
                return last_update["edited_message"]["chat"]["id"]
            elif (
                "channel_post" in last_update and "chat" in last_update["channel_post"]
            ):
                return last_update["channel_post"]["chat"]["id"]
            elif (
                "edited_channel_post" in last_update
                and "chat" in last_update["edited_channel_post"]
            ):
                return last_update["edited_channel_post"]["chat"]["id"]
    return None


def get_latest_commit_messages(n=1):
    """Fetches the latest n commit messages from the Git repository."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=%B"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching latest commit messages: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Telegram Bot Script")
    parser.add_argument(
        "--job",
        choices=["send_message"],
        required=True,
        help="Job to perform",
    )
    args = parser.parse_args()

    if args.job == "send_message":
        if TELEGRAM_BOT_API_KEY and TELEGRAM_CHAT_ID:
            commit_messages = get_latest_commit_messages()
            if commit_messages:
                message = f"Blog Updated. Commit messages:\n{commit_messages}\nBlog Link: https://lzwjava.github.io"
                send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            else:
                print("Could not retrieve the latest commit messages.")
        else:
            print("TELEGRAM_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")


if __name__ == "__main__":
    main()
