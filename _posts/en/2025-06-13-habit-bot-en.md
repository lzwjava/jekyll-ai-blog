---
audio: false
generated: false
image: false
lang: en
layout: post
title: Building a Habit Bot With Mistral
translated: false
type: post
---

In this blog post, we explore the creation of a Habit Bot designed to send automated reminders using Python and GitHub Actions. This bot leverages the Telegram API for messaging and integrates with Mistral AI to generate contextually relevant prompts. By scheduling tasks with GitHub Actions, the bot encourages consistent habits through timely notifications. We'll walk through the setup, from environment configuration to scripting and deployment, providing a practical guide for automating your habit tracking system.

## Code

```python
import os
import requests
import argparse
import re
import datetime
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv()

# Environment variables
TELEGRAM_HABIT_BOT_API_KEY = os.environ.get("TELEGRAM_HABIT_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

# Telegram message length limit
TELEGRAM_MAX_LENGTH = 4096

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_HABIT_BOT_API_KEY or TELEGRAM_CHAT_ID not set.")
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Remove Markdown asterisks and URLs to ensure Telegram compatibility
    message_no_stars = message.replace('*', '')
    url_pattern = re.compile(r'(https?://[^\s]+)')
    message_no_links = url_pattern.sub('', message_no_stars)
    # Split message if it exceeds Telegram's length limit
    messages = []
    msg = message_no_links
    while len(msg) > TELEGRAM_MAX_LENGTH:
        split_idx = msg.rfind('\n', 0, TELEGRAM_MAX_LENGTH)
        if split_idx == -1 or split_idx < TELEGRAM_MAX_LENGTH // 2:
            split_idx = TELEGRAM_MAX_LENGTH
        messages.append(msg[:split_idx])
        msg = msg[split_idx:]
    messages.append(msg)
    success = True
    for part in messages:
        params = {
            "chat_id": chat_id,
            "text": part,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            print(f"Successfully sent Telegram message part ({len(part)} chars).")
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            success = False
    return success


def call_mistral_api(prompt, model="mistral-large-latest"):
    """Calls the Mistral API to generate a response."""
    if not MISTRAL_API_KEY:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,  # Adjust temperature for creativity
        "max_tokens": 300  # Limit response length
    }
    try:
        print(f"Calling Mistral API with model: {model}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('choices'):
            content = response_json['choices'][0]['message']['content']
            print(f"Mistral API Content: {content}")
            return content
        print(f"Mistral API Error: Invalid response format: {response_json}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        return None

def generate_copilot_message():
    """Generates a technical prompt sentence encouraging Copilot use via Mistral API."""
    prompt = (
        f"Generate a unique, specific technical prompt sentence for a user backend engineer"
        "Randomly select one technology from: Java, Spring Boot, Control-M, IBM WebSphere, Maven, multithreading, Nexus, Windows, JVM, Service-NOW, Python, AI or DevOps, Linux. Algorithms and Banking "
        "Format as 'Stuck on [specific challenge]? Ask Copilot!' or 'Struggling with [task]? Find Copilot to help!' "
        "Ensure variety in challenges (e.g., configuration, debugging, optimization). "
        "Keep it under 300 characters, avoid Markdown or URLs, and output only the sentence."
    )
    message = call_mistral_api(prompt)
    if message:
        return message.strip()[:300]
    return "Stuck on configuring Control-M order date? Ask Copilot!"

def main():
    parser = argparse.ArgumentParser(description="Telegram Habit Reminder Bot")
    parser.add_argument("--job", choices=["send_reminder", "send_message"], required=True, help="Job to perform")
    parser.add_argument("--message", type=str, help="Message to send for 'send_message' job")
    args = parser.parse_args()

    if args.job == "send_reminder":
        if TELEGRAM_HABIT_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = generate_copilot_message()
            send_telegram_message(TELEGRAM_HABIT_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
        else:
            print("Error: TELEGRAM_HABIT_BOT_API_KEY or TELEGRAM_CHAT_ID not set.")
    elif args.job == "send_message":
        if TELEGRAM_HABIT_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "Default test message from the bot!"
            send_telegram_message(TELEGRAM_HABIT_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
        else:
            print("Error: TELEGRAM_HABIT_BOT_API_KEY or TELEGRAM_CHAT_ID not set.")

if __name__ == "__main__":
    main()
```

## GitHub Action

```yaml
name: Habit

on:
  schedule:
    # Run every 10 minutes (0, 10, 20, 30, 40, 50 minutes past the hour) from 05:00–13:00 UTC, Mon–Fri
    # 05:00–13:00 UTC = 13:00–21:00 Beijing time (UTC+8)
    - cron: '0,10,20,30,40,50 5-13 * * 1-5'

  workflow_dispatch:
    # Allow manual trigger for testing
    inputs:
      message:
        description: 'Custom message for testing (optional)'
        required: false
        default: 'Test message from GitHub Actions.'
      job:
        description: 'Job to run (optional)'
        required: false
        default: 'send_message'

  push:
    branches: ["main"]
    paths:
      - 'scripts/bot/habit_bot.py'
      - '.github/workflows/habit_reminder.yml'

concurrency:
  group: 'habit_reminder'
  cancel-in-progress: false

jobs:
  habit_reminder_job:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_HABIT_BOT_API_KEY: ${{ secrets.TELEGRAM_HABIT_BOT_API_KEY }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 5

      - name: Set up Python 3.13
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run habit reminder script (Scheduled)
        run: python scripts/bot/habit_bot.py --job send_reminder
        if: github.event_name == 'schedule'

      - name: Run habit reminder script (Manual Trigger)
        run: python scripts/bot/habit_bot.py --job ${{ github.event.inputs.job }} --message "${{ github.event.inputs.message }}"
        if: github.event_name == 'workflow_dispatch'

      - name: Notify on push to main branch
        run: python scripts/bot/habit_bot.py --job send_message --message "Code changes for habit bot pushed to main branch."
        if: github.event_name == 'push'

```