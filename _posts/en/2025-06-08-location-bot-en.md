---
audio: false
generated: false
image: false
lang: en
layout: post
title: Automating Your Punch Card with a Telegram Location Bot
translated: false
type: post
---

Ever wish your daily "punch card" was less of a chore? I certainly did. That's why I built a personal Telegram bot that uses location tracking to automate office arrival notifications and remind me about those crucial check-ins. This post dives into how I combined Python with GitHub Actions to create a seamless, hands-free system, keeping me informed right when I need it, all based on my location.


```yml
name: Hourly Location Check

on:
  schedule:
    # Run every hour, on the hour, between 11 AM and 11 PM, on weekdays (Monday-Friday)
    # The time is in UTC. Singapore time (SGT) is UTC+8.
    # So, 11 AM SGT is 03:00 UTC, and 11 PM SGT is 15:00 UTC.
    # Therefore, we need to schedule from 03:00 to 15:00 UTC.
    - cron: '0 3-15 * * 1-5'

    # Reminder to START sharing live location: Wednesday 11 AM SGT (3 AM UTC)
    # Current time: Sunday, June 8, 2025 at 5:10:58 PM +08 (SGT)
    # For Wednesday 11 AM SGT (UTC+8): 11 - 8 = 3 AM UTC.
    - cron: '0 3 * * 3' # 3 for Wednesday

    # Reminder to STOP sharing live location: Friday 11 PM SGT (3 PM UTC)
    # Current time: Sunday, June 8, 2025 at 5:10:58 PM +08 (SGT)
    # For Friday 11 PM SGT (UTC+8): 23 - 8 = 15 PM UTC.
    - cron: '0 15 * * 5' # 5 for Friday

  workflow_dispatch:  # Allows manual triggering of the workflow
  push:
    branches: ["main"]
    paths:
      - 'scripts/release/location_bot.py' # Corrected path to your script
      - '.github/workflows/location.yml' # Path to this workflow file

concurrency:
  group: 'location'
  cancel-in-progress: false

jobs:
  check_and_notify:
    runs-on: ubuntu-latest
    env:
      TELEGRAM_LOCATION_BOT_API_KEY: ${{ secrets.TELEGRAM_LOCATION_BOT_API_KEY }}

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 5 # Fetch only the last 5 commits for efficiency

    - name: Set up Python 3.13.2
      uses: actions/setup-python@v4
      with:
        python-version: "3.13.2" # Specify the exact Python version

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        # Assuming you have a requirements.simple.txt in your repo root.
        # If not, use: pip install requests python-dotenv
        pip install -r requirements.simple.txt 

    - name: Run location check script (Scheduled)
      run: python scripts/release/location_bot.py --job check_location
      # This step will run on scheduled triggers for the hourly check
      if: github.event.schedule == '0 3-15 * * 1-5' # Match the hourly cron schedule

    - name: Reminder to START sharing live location
      run: python scripts/release/location_bot.py --job start_sharing_message
      if: github.event.schedule == '0 3 * * 3' # Matches Wednesday 11 AM SGT cron

    - name: Reminder to STOP sharing live location
      run: python scripts/release/location_bot.py --job stop_sharing_message
      if: github.event.schedule == '0 15 * * 5' # Matches Friday 11 PM SGT cron

    - name: Run Telegram script for test message (Manual Trigger)
      run: python scripts/release/location_bot.py --job send_message --message "This is a manual trigger test message from GitHub Actions."
      if: github.event_name == 'workflow_dispatch'

    - name: Run Telegram script for push to main branch
      run: python scripts/release/location_bot.py --job send_message --message "Code changes for location bot pushed to main branch."
      if: github.event_name == 'push'
```

```python
import os
import requests
from dotenv import load_dotenv
import json
import subprocess
import argparse
import math
import time # For potential future continuous monitoring

load_dotenv()

# New: Specific API key for the location bot
TELEGRAM_LOCATION_BOT_API_KEY = os.environ.get("TELEGRAM_LOCATION_BOT_API_KEY") # Ensure this is set in your .env
TELEGRAM_CHAT_ID = "610574272" # This chat ID is for sending the notification message

# Define your office coordinates
OFFICE_LATITUDE = 23.135368
OFFICE_LONGITUDE = 113.32952

# Proximity radius in meters
PROXIMITY_RADIUS_METERS = 300

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" # Using Markdown for bold text in the message
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.status_code} - {response.text}")

def get_latest_location(bot_token):
    """Retrieves the latest live location update from the bot."""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    # Offset to get only new updates after the last processed one (for continuous polling)
    # For a simple run-once script, we'll just get the latest, but for polling, you'd manage an offset.
    params = {"offset": -1} # Get the very last update
    response = requests.get(url, params=params)
    print("GetUpdates Response:", response) # Debugging
    if response.status_code == 200:
        updates = response.json()
        print("GetUpdates JSON:", json.dumps(updates, indent=4)) # Debugging
        if updates['result']:
            last_update = updates['result'][-1]
            # Prioritize edited_message for live locations
            if 'edited_message' in last_update and 'location' in last_update['edited_message']:
                return last_update['edited_message']['location'], last_update['edited_message']['chat']['id']
            elif 'message' in last_update and 'location' in last_update['message']:
                # Handle initial live location messages or static location shares
                return last_update['message']['location'], last_update['message']['chat']['id']
    return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in meters.
    """
    R = 6371000  # Radius of Earth in meters

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def main():
    parser = argparse.ArgumentParser(description="Telegram Bot Script")
    # Updated choices for --job argument
    parser.add_argument('--job', choices=['get_chat_id', 'send_message', 'check_location', 'start_sharing_message', 'stop_sharing_message'], required=True, help="Job to perform")
    # Added --message argument for 'send_message' job
    parser.add_argument('--message', type=str, help="Message to send for 'send_message' job")
    # Added --test argument for 'check_location' job
    parser.add_argument('--test', action='store_true', help="For 'check_location' job, force sending a message regardless of proximity.")
    args = parser.parse_args()

    if args.job == 'get_chat_id':
        bot_token = TELEGRAM_LOCATION_BOT_API_KEY
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json()
            print(json.dumps(updates, indent=4))
            if updates['result']:
                last_update = updates['result'][-1]
                chat_id = None
                if 'message' in last_update and 'chat' in last_update['message']:
                    chat_id = last_update['message']['chat']['id']
                elif 'edited_message' in last_update and 'chat' in last_update['edited_message']:
                    chat_id = last_update['edited_message']['chat']['id']
                elif 'channel_post' in last_update and 'chat' in last_update['channel_post']:
                    chat_id = last_update['channel_post']['chat']['id']
                elif 'edited_channel_post' in last_update and 'chat' in last_update['edited_channel_post']:
                    chat_id = last_update['edited_channel_post']['chat']['id']

                if chat_id:
                    print(f"Chat ID: {chat_id}")
                else:
                    print("Could not retrieve chat ID from the last update.")
            else:
                print("No updates found.")
        else:
            print(f"Error fetching updates: {response.status_code} - {response.text}")

    elif args.job == 'send_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "This is a default test message from your Telegram bot script!"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print(f"Message sent successfully: {message}")
        else:
            print("TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")

    elif args.job == 'start_sharing_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = "⚠️ *Reminder:* Please start sharing your live location to the bot!"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print("Start sharing reminder sent.")
        else:
            print("TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")

    elif args.job == 'stop_sharing_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = "✅ *Reminder:* You can stop sharing your live location now."
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print("Stop sharing reminder sent.")
        else:
            print("TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")

    elif args.job == 'check_location':
        if not TELEGRAM_LOCATION_BOT_API_KEY or not TELEGRAM_CHAT_ID:
            print("TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID must be set for location checks.")
            return

        user_location, location_chat_id = get_latest_location(TELEGRAM_LOCATION_BOT_API_KEY)

        if user_location:
            current_latitude = user_location['latitude']
            current_longitude = user_location['longitude']

            distance = haversine_distance(
                OFFICE_LATITUDE, OFFICE_LONGITUDE,
                current_latitude, current_longitude
            )

            print(f"Current location: ({current_latitude}, {current_longitude})")
            print(f"Distance to office: {distance:.2f} meters")

            needs_punch_card = distance <= PROXIMITY_RADIUS_METERS

            if needs_punch_card:
                print(f"You are within {PROXIMITY_RADIUS_METERS}m of the office!")
                notification_message = (
                    f"🎉 *Arrived Office!* 🎉\n"
                    f"Time to Punch card in WeCom.\n"
                    f"Your current distance from office: {distance:.2f}m."
                )
            else:
                print(f"You are outside the {PROXIMITY_RADIUS_METERS}m office circle.")
                # Message for when outside the radius
                notification_message = (
                    f"📍 You are *outside* the office proximity ({PROXIMITY_RADIUS_METERS}m).\n"
                    f"No punch card needed at this time.\n"
                    f"Your current distance from office: {distance:.2f}m."
                )

            # Send message if within proximity OR if --test flag is used
            if needs_punch_card or args.test:
                send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, notification_message)
            else:
                # If not within proximity AND not in test mode, just print to console (no Telegram message)
                print("Not within proximity and not in test mode, no message sent to Telegram.")
        else:
            print("Could not retrieve your latest location. Make sure you are sharing live location with the bot.")

if __name__ == '__main__':
    main()
```

---

Update: This is not good because you need to share your live location with the bot.