---
audio: false
generated: true
lang: en
layout: post
title: Punch Card Reminders with Supabase
translated: false
type: note
---

I'll help you modify the existing GitHub Actions workflow and Python script to implement punch card reminders from Wednesday to Friday, with reminders every 5 minutes during 12 PM to 3 PM (punch in) and 6 PM to 9 PM (punch out) SGT, stopping when a "punch" message is received via Telegram. We'll use Supabase to track punch states to prevent redundant reminders.

Below are the complete instructions and code:

---

### GitHub Actions Workflow
The workflow needs to run every 5 minutes during the specified time windows in SGT (UTC+8):
- Punch in: 12 PM to 3 PM SGT = 4 AM to 7 AM UTC
- Punch out: 6 PM to 9 PM SGT = 10 AM to 1 PM UTC
- Days: Wednesday to Friday (3-5 in cron syntax)

We'll use a single cron schedule combining these hours and let the script determine the action.

{% raw %}
```yaml
name: Punch Card Reminders

on:
  schedule:
    # Run every 5 minutes from 4-7 AM and 10 AM-1 PM UTC, Wed-Fri
    # 4-7 AM UTC = 12 PM-3 PM SGT, 10 AM-1 PM UTC = 6 PM-9 PM SGT
    - cron: '*/5 4-7,10-13 * * 3-5'

  workflow_dispatch:
    inputs:
      job_name:
        description: 'Job to run (punch_reminder, send_message)'
        required: true
        default: 'punch_reminder'
      message:
        description: 'Custom message for send_message job (optional)'
        required: false
        default: 'This is a manual trigger test message from GitHub Actions.'

  push:
    branches: ["main"]
    paths:
      - 'scripts/release/location_bot.py'
      - '.github/workflows/location.yml'

concurrency:
  group: 'punch_reminder'
  cancel-in-progress: false

jobs:
  punch_reminder_job:
    runs-on: ubuntu-latest
    environment: github-pages
    env:
      TELEGRAM_LOCATION_BOT_API_KEY: ${{ secrets.TELEGRAM_LOCATION_BOT_API_KEY }}
      SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
      SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 5

    - name: Set up Python 3.13.2
      uses: actions/setup-python@v4
      with:
        python-version: "3.13.2"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.simple.txt

    - name: Run punch reminder script (Scheduled)
      run: python scripts/release/location_bot.py --job punch_reminder
      if: github.event_name == 'schedule'

    - name: Run punch reminder script (Manual Trigger)
      run: python scripts/release/location_bot.py --job punch_reminder
      if: github.event_name == 'workflow_dispatch' && github.event.inputs.job_name == 'punch_reminder'

    - name: Run Telegram script for custom message (Manual Trigger)
      run: python scripts/release/location_bot.py --job send_message --message "${{ github.event.inputs.message }}"
      if: github.event_name == 'workflow_dispatch' && github.event.inputs.job_name == 'send_message'

    - name: Notify on push to main branch
      run: python scripts/release/location_bot.py --job send_message --message "Code changes for punch reminder bot pushed to main branch."
      if: github.event_name == 'push'
```
{% endraw %}

---

### Python Script
The script will:
- Check the current SGT time to determine if it's punch in or punch out window
- Use Supabase to track punch states
- Fetch Telegram updates for "punch" messages
- Send reminders if the punch hasn't been recorded

Update your `requirements.simple.txt` to include:
```
requests
supabase
pytz
```

Here's the modified script:

```python
import os
import requests
import datetime
import pytz
from supabase import create_client
import argparse

# Load environment variables
TELEGRAM_LOCATION_BOT_API_KEY = os.environ.get("TELEGRAM_LOCATION_BOT_API_KEY")
TELEGRAM_CHAT_ID = "610574272"  # Your chat ID

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.status_code} - {response.text}")

def send_reminder(action):
    """Sends a punch reminder message."""
    message = f"⏰ *Reminder:* Please punch {action.replace('_', ' ')} by sending 'punch' to this bot."
    send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)

def main():
    parser = argparse.ArgumentParser(description="Telegram Punch Reminder Bot")
    parser.add_argument('--job', choices=['punch_reminder', 'send_message'], required=True, help="Job to perform")
    parser.add_argument('--message', type=str, help="Message to send for 'send_message' job")
    args = parser.parse_args()

    if args.job == 'send_message':
        if TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = args.message if args.message else "Default test message from your bot!"
            send_telegram_message(TELEGRAM_LOCATION_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print(f"Message sent: {message}")
        else:
            print("TELEGRAM_LOCATION_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")
        return

    elif args.job == 'punch_reminder':
        # Initialize Supabase
        supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

        # Get current time in SGT (UTC+8)
        sgt = pytz.timezone('Asia/Singapore')
        now_utc = datetime.datetime.utcnow()
        now_sgt = now_utc.replace(tzinfo=pytz.utc).astimezone(sgt)
        today_sgt = now_sgt.date()

        # Define time windows
        punch_in_start = datetime.time(12, 0)  # 12 PM SGT
        punch_in_end = datetime.time(15, 0)    # 3 PM SGT
        punch_out_start = datetime.time(18, 0) # 6 PM SGT
        punch_out_end = datetime.time(21, 0)   # 9 PM SGT

        current_time = now_sgt.time()

        # Determine current window
        if punch_in_start <= current_time <= punch_in_end:
            window = 'punch_in'
        elif punch_out_start <= current_time <= punch_out_end:
            window = 'punch_out'
        else:
            window = None

        if not window:
            print("Outside punch reminder windows.")
            return

        # Fetch today's punch record
        response = supabase.table('punch_records').select('*').eq('date', str(today_sgt)).execute()
        punch_record = response.data[0] if response.data else None

        # Check if punch is already done
        if window == 'punch_in' and punch_record and punch_record['punch_in_time']:
            print("Already punched in today.")
            return
        if window == 'punch_out' and punch_record and punch_record['punch_out_time']:
            print("Already punched out today.")
            return

        # Fetch last processed Telegram update ID
        state_response = supabase.table('telegram_state').select('last_update_id').eq('id', 1).execute()
        last_update_id = state_response.data[0]['last_update_id'] if state_response.data else 0

        # Get new Telegram updates
        url = f"https://api.telegram.org/bot{TELEGRAM_LOCATION_BOT_API_KEY}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 0}
        response = requests.get(url, params=params)
        updates = response.json().get('result', [])

        max_update_id = last_update_id
        for update in updates:
            if update['update_id'] > max_update_id:
                max_update_id = update['update_id']
            if ('message' in update and
                update['message'].get('text', '').lower() == 'punch' and
                str(update['message']['chat']['id']) == TELEGRAM_CHAT_ID):
                # Process "punch" message
                if window == 'punch_in':
                    if not punch_record:
                        supabase.table('punch_records').insert({
                            'date': str(today_sgt),
                            'punch_in_time': now_utc.isoformat()
                        }).execute()
                    else:
                        supabase.table('punch_records').update({
                            'punch_in_time': now_utc.isoformat()
                        }).eq('date', str(today_sgt)).execute()
                elif window == 'punch_out':
                    if not punch_record:
                        supabase.table('punch_records').insert({
                            'date': str(today_sgt),
                            'punch_out_time': now_utc.isoformat()
                        }).execute()
                    else:
                        supabase.table('punch_records').update({
                            'punch_out_time': now_utc.isoformat()
                        }).eq('date', str(today_sgt)).execute()

        # Update last_update_id
        if max_update_id > last_update_id:
            supabase.table('telegram_state').update({
                'last_update_id': max_update_id
            }).eq('id', 1).execute()

        # Refetch punch record to check latest state
        response = supabase.table('punch_records').select('*').eq('date', str(today_sgt)).execute()
        punch_record = response.data[0] if response.data else None

        # Send reminder if punch not recorded
        if window == 'punch_in' and (not punch_record or not punch_record['punch_in_time']):
            send_reminder('punch_in')
        elif window == 'punch_out' and (not punch_record or not punch_record['punch_out_time']):
            send_reminder('punch_out')

if __name__ == '__main__':
    main()
```

---

### Supabase Setup
We'll create two tables in Supabase to manage punch states and Telegram updates.

#### SQL Instructions
Run these SQL commands in the Supabase SQL Editor:

```sql
-- Table to store daily punch records
CREATE TABLE punch_records (
    date DATE PRIMARY KEY,
    punch_in_time TIMESTAMP,
    punch_out_time TIMESTAMP
);
users

-- Initialize telegram_state with a single row
INSERT INTO telegram_state (id, last_update_id) VALUES (1, 0);
```

#### Steps to Execute
1. Log into your Supabase dashboard.
2. Navigate to **SQL Editor**.
3. Paste and run the SQL code above to create and initialize the tables.

---

### Environment Variables
Ensure these secrets are set in your GitHub repository under **Settings > Secrets and variables > Actions > Secrets**:
- `TELEGRAM_LOCATION_BOT_API_KEY`: Your Telegram bot token.
- `SUPABASE_URL`: Your Supabase project URL (e.g., `https://xyz.supabase.co`).
- `SUPABASE_KEY`: Your Supabase anon key (found in **Settings > API**).

---

### How It Works
1. **Schedule**: The workflow runs every 5 minutes during 12 PM-3 PM and 6 PM-9 PM SGT (adjusted to UTC) on Wednesday to Friday.
2. **Time Check**: The script checks the current SGT time to determine if it's in the punch in or punch out window.
3. **State Management**:
   - Checks `punch_records` for today's punches.
   - If already punched (e.g., `punch_in_time` is set during 12 PM-3 PM), no reminder is sent.
4. **Telegram Updates**:
   - Fetches updates since the last processed `update_id`.
   - If a "punch" message is found, updates `punch_records` with the current time for punch in or out.
   - Updates `telegram_state` with the latest `update_id`.
5. **Reminders**: Sends a reminder every 5 minutes if the punch hasn't been recorded for the current window.

---

### Testing
- **Manual Trigger**: Use `workflow_dispatch` with `job_name: punch_reminder` to test manually.
- **Telegram**: Send "punch" to your bot during the window to stop reminders for that session.
- **Supabase**: Check the `punch_records` table to verify punch times are recorded.

This setup replaces the location-based logic with time-based punch reminders, leveraging Supabase for persistent state management within GitHub Actions' constraints.
