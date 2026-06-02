---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Slack Setup Review: Completed and Pending"
translated: false
type: note
---

Here's a comprehensive review of the Slack setup steps we've completed and what's still needed: 🦞

## ✅ Completed Steps

1. **Slack App Created** — You created a Slack app in your workspace.
2. **Bot Token Configured** — Added the `xoxb-...` bot token to OpenClaw.
3. **App-Level Token Configured** — Added the `xapp-...` app-level token for socket mode.
4. **Gateway Restarted** — The gateway restarted and Slack socket mode is now **connected**.
5. **Plugin Loaded** — The Slack plugin shows as **loaded** in the plugin list.

## 🔧 Still Needed (Slack-Side Configuration)

### 1. Event Subscriptions
In your Slack app dashboard ([api.slack.com/apps](https://api.slack.com/apps)):
- Go to **Event Subscriptions**
- Turn **Enable Events** to **On**
- Under **Subscribe to bot events**, add:
  - `message.channels` — for public channel messages
  - `message.groups` — for private channel messages
  - `message.im` — for direct messages
  - `message.mpim` — for group DMs
  - `app_mention` — for when someone mentions the bot
- Click **Save Changes**

### 2. OAuth Scopes (Verify)
In **OAuth & Permissions** → **Bot Token Scopes**, ensure these are added:
- `chat:write`
- `channels:history`
- `channels:read`
- `groups:history`
- `groups:read`
- `im:history`
- `im:read`
- `im:write`
- `mpim:history`
- `mpim:read`
- `mpim:write`
- `app_mentions:read`

### 3. Invite Bot to Channel
In each Slack channel where you want the bot to respond:
- Type `/invite @YourBotName` to add it to the channel

### 4. Socket Mode (Verify)
In **Socket Mode** on the Slack app dashboard:
- Make sure Socket Mode is **Enabled**
- The app-level token should already be active

## 🧪 Testing
After completing the above:
1. Send a message in a channel where the bot is invited.
2. Check the logs with `tail -f /tmp/openclaw/openclaw-2026-04-05.log | grep slack` to see if events are coming through.

Want me to check the logs again after you've verified these settings?
