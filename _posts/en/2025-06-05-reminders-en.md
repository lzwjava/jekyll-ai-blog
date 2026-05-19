---
audio: false
generated: false
image: false
lang: en
layout: post
title: Streamline Reminders via Telegram
translated: false
type: post
---

In this project, I set up an automated reminder system using GitHub Actions and a Telegram bot to keep my daily and monthly tasks on track. By leveraging cron schedules, I configured reminders for work-related tasks like punching in on WeCom, submitting timesheets, and checking salaries, as well as personal tasks such as visiting family, shopping on JD.com, and even watching TV with my partner. The system uses a Python script to send messages via Telegram's Bot API, with environment variables securely stored in GitHub Secrets. This setup ensures I never miss critical deadlines or personal commitments, blending technology with everyday life for maximum efficiency.

```yaml
name: Reminders

on:
  schedule:
    # Runs every 2 hours from 12 PM to 8 PM (Beijing time, UTC+8) from Wednesday to Friday.
    - cron: '0 4,6,8,10,12 * * 3-5'
    # Runs on the 27th of every month at 12 PM (Beijing time, UTC+8).
    - cron: '0 4 27 * *'
    # Runs on the 30th of every month at 2 PM (Beijing time, UTC+8).
    - cron: '0 6 30 * *'
    # Runs every day at 1 AM Beijing time (5 PM UTC the previous day).
    - cron: '0 17 * * *'
    # Runs every day at 11 AM Beijing time (3 AM UTC).
    - cron: '0 3 * * *'
    # Reminds to go to parents' house next day: 9 PM Beijing Time (1 PM UTC) on Tue, Wed, Thu.
    - cron: '0 13 * * 2-4'
    # Reminds to go to own house next day: 9 PM Beijing Time (1 PM UTC) on Sun, Mon, Fri, Sat.
    - cron: '0 13 * * 0,1,5,6'
    # Reminds to buy fresh produce direct from the source in JD.com: 9 PM Beijing Time (1 PM UTC) on Wednesday.
    - cron: '0 13 * * 3'
    # Reminds to buy quick delivery food from JD.com: 9 PM Beijing Time (1 PM UTC) on Friday.
    - cron: '0 13 * * 5'
    # Reminds about associate degree exam in March, April, September, and October every Monday at 1 PM Beijing Time (5 AM UTC).
    - cron: '0 5 * 3,4,9,10 1'
    # Reminds to submit weekly timesheet every Friday at 5 PM Taipei time (9 AM UTC).
    - cron: '0 9 * * 5'
    # Reminds to submit vendor timesheet on the 25th of every month at 12 AM Taipei time (4 PM UTC previous day).
    - cron: '0 16 25 * *'
    # Reminds to ask family to support mortgage payment on the 16th of every month at 9 PM Taipei time (1 PM UTC).
    - cron: '0 13 16 * *'
    # Reminds to watch TV with partner every Friday, Saturday, and Sunday at 10 PM Taipei time (2 PM UTC).
    - cron: '0 14 * * 5,6,0'
    # Reminds to remove parking permit sticker at 2 AM Beijing time (6 PM UTC) on Wed, Thu, Fri.
    - cron: '0 18 * * 3,4,5'
  workflow_dispatch:  # Allows manual triggering

concurrency:
  group: 'reminders'
  cancel-in-progress: false

jobs:
  send-reminders:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_BOT2_API_KEY: ${{ secrets.TELEGRAM_BOT2_API_KEY }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: Set up Python 3.10.x
        uses: actions/setup-python@v4
        with:
          python-version: "3.10.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.simple.txt

      - name: Run Telegram script for daily punch card reminders
        run: python scripts/release/reminders_bot.py --job send_message --message "Punch card in WeCom"
        if: github.event.schedule == '0 4,6,8,10,12 * * 3-5'

      - name: Run Telegram script for monthly mortgage reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Prepare house mortgage deduction"
        if: github.event.schedule == '0 4 27 * *'

      - name: Run Telegram script for monthly salary check reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Check salary"
        if: github.event.schedule == '0 6 30 * *'

      - name: Run Telegram script for sleep reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Time to sleep!"
        if: github.event.schedule == '0 17 * * *'

      - name: Run Telegram script for wake up reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Time to wake up!"
        if: github.event.schedule == '0 3 * * *'

      - name: Run Telegram script for parents' house reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Go to house of parents tomorrow!"
        if: github.event.schedule == '0 13 * * 2-4'

      - name: Run Telegram script for own house reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Go to your house tomorrow!"
        if: github.event.schedule == '0 13 * * 0,1,5,6'

      - name: Run Telegram script for JD.com fresh produce reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Buy fresh produce direct from the source in JD.com!"
        if: github.event.schedule == '0 13 * * 3'

      - name: Run Telegram script for JD.com quick delivery food reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Buy quick delivery food from JD.com!"
        if: github.event.schedule == '0 13 * * 5'

      - name: Run Telegram script for associate degree exam reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Register associate degree exam"
        if: github.event.schedule == '0 5 * 3,4,9,10 1'

      - name: Run Telegram script for weekly timesheet reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Submit weekly timesheet"
        if: github.event.schedule == '0 9 * * 5'

      - name: Run Telegram script for vendor timesheet reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Submit vendor timesheet"
        if: github.event.schedule == '0 16 25 * *'

      - name: Run Telegram script for family mortgage support reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Ask family to support mortgage payment"
        if: github.event.schedule == '0 13 16 * *'

      - name: Run Telegram script for watch TV with partner reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Time to watch TV with your partner!"
        if: github.event.schedule == '0 14 * * 5,6,0'

      - name: Run Telegram script for car window paper stick reminder
        run: python scripts/release/reminders_bot.py --job send_message --message "Remove parking permit sticker from car window"
        if: github.event.schedule == '0 18 * * 3,4,5'

      - name: Run Telegram script for test message
        run: python scripts/release/reminders_bot.py --job send_message --message "This is a test message from GitHub Actions."
        if: github.event_name == 'workflow_dispatch'
```

```python
import os
import requests
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

TELEGRAM_BOT2_API_KEY = os.environ.get("TELEGRAM_BOT2_API_KEY")
TELEGRAM_CHAT_ID = "610574272"

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.status_code} - {response.text}")

def get_chat_id(bot_token):
    """Retrieves the chat ID of the last message sent to the bot."""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        print(json.dumps(updates, indent=4))
        if updates['result']:
            chat_id = updates['result'][-1]['message']['chat']['id']
            return chat_id
    return None

def send_reminder(message):
    """Sends a reminder message to Telegram."""
    if TELEGRAM_BOT2_API_KEY and TELEGRAM_CHAT_ID:
        send_telegram_message(TELEGRAM_BOT2_API_KEY, TELEGRAM_CHAT_ID, f"Reminder: {message}")
    else:
        print("TELEGRAM_BOT2_API_KEY and TELEGRAM_CHAT_ID are not set.")

def main():
    parser = argparse.ArgumentParser(description="Telegram Bot Script")
    parser.add_argument('--job', choices=['get_chat_id', 'send_message'], required=True, help="Job to perform")
    parser.add_argument('--message', help="Custom message to send", default=None)
    args = parser.parse_args()

    if args.job == 'get_chat_id':
        bot_token = TELEGRAM_BOT2_API_KEY
        chat_id = get_chat_id(bot_token)
        if chat_id:
            print(f"Chat ID: {chat_id}")
        else:
            print("Could not retrieve chat ID.")

    elif args.job == 'send_message':
        if args.message:
            send_reminder(args.message)
        else:
            print("No message provided for send_message job.")
            
if __name__ == '__main__':
    main()
```