---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Telegram Bot Token 409 Conflict
translated: false
type: note
---

Here's the review — found **two distinct issues**:

---

**Issue 1: `getUpdates` 409 Conflict (🔴 Critical)**
The Telegram bot token is being used by **two things simultaneously**:

- OpenClaw's Telegram plugin (long polling)
- Your `telegram_bot.py` in blog-source (which also calls `getUpdates`)

They fight over the same polling connection → OpenClaw keeps getting `409 Conflict` and stalling.

**Issue 2: Group config fixed ✅**
The `channels.telegram.groups` approach worked — no more "Invalid allowFrom" errors in recent logs. The group "blog" is now recognized.

---

**To fix the 409 conflict**, you need to **stop your `telegram_bot.py` from polling**. Since OpenClaw now handles push messages to the group, your existing push script should only run on-demand (e.g., git hook triggered), not as a continuous poller.

The simplest fix — in your `telegram_bot.py`, comment out or remove the `get_chat_id` job that calls `getUpdates`, since you've already obtained the chat ID and OpenClaw now owns the Telegram connection:

```python
# Comment out or delete the getUpdates polling part:
# def get_chat_id(bot_token):
#     url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
#     ...
```

Want me to make that change for you?
