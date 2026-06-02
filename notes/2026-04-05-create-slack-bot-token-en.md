---
audio: false
generated: true
image: false
lang: en
layout: post
title: Create a Slack Bot Token
translated: false
type: note
---

I'll guide you through creating a Slack bot token. 🦞

1. **Go to** [https://api.slack.com/apps](https://api.slack.com/apps) and click **Create New App**.
2. Choose **From scratch**, give it a name (e.g., "OpenClaw Bot"), and pick your workspace.
3. In the left sidebar, go to **OAuth & Permissions**.
4. Under **Scopes**, add these bot token scopes:
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
5. Scroll up and click **Install to Workspace**.
6. After installation, copy the **Bot User OAuth Token** (starts with `xoxb-`).

Once you have that token, paste it here and I'll configure OpenClaw to use it.
