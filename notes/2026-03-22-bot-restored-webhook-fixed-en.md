---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bot Capabilities Restored and Webhook Fixed
translated: false
type: note
---

Everything's up. Gateway restarted, webhook listening on `0.0.0.0:8788`, group policy set to `open`. Let me test the full flow from the container:Webhook accepted from the container. Let me check if OpenClaw processed it:The pipeline is working! The test message was received (it flagged as "replayed" because I used the same message ID earlier). Here's the summary of where we are:

**Working:**
- ✅ Nextcloud Talk plugin installed & loaded
- ✅ Bot registered in Nextcloud (`talk:bot:install`)
- ✅ Webhook listener on `0.0.0:8788`
- ✅ UFW firewall rule added for port 8788
- ✅ Group policy set to `open`
- ✅ Webhook reaches OpenClaw from the container

**The issue:** When you sent your message in Talk, the bot might not have triggered because the webhook URL was set *before* the UFW rule existed, and Nextcloud may have cached a failure. Let me check:Found the problem — the bot was installed with only `--feature reaction` (feature 2), but the DB shows feature 8 (assistant only). It needs the `message` capability to receive chat messages. Let me reinstall it:Fixed! The bot now has **webhook + response + reaction** capabilities. Go send another message in the Talk room — this time it should actually trigger OpenClaw.