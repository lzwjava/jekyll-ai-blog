---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable OpenClaw Bot in Nextcloud Talk
translated: false
type: note
---

**Question:** How do I enable the OpenClaw bot (ID: 4) in a Nextcloud Talk conversation? I can't find it in the Talk UI — I only see the admin panel.

**Answer:**

There is **no visible "bot list" in the Nextcloud Talk UI** for enabling bots. For security reasons, bots can only be added and managed via the command line using `occ` commands. The UI only shows bots *after* they've been enabled per-conversation via CLI first.

You need to do this via the **command line on your Nextcloud server** (or Docker container).

---

## Step 1: Get Your Conversation Token

Open the Talk conversation you want the bot in. Look at the URL:
```
http://192.168.1.36:8080/apps/spreed/#/XXXXXXXX
```
That `XXXXXXXX` at the end is your **room token**.

---

## Step 2: Enable the Bot in That Conversation

Run this on your Nextcloud server (or inside Docker):

```bash
# If running in Docker:
docker exec -it -u 33 <nextcloud_container_name> /var/www/html/occ talk:bot:setup 4 <ROOM_TOKEN>
```

Replace `<ROOM_TOKEN>` with the token from Step 1.

The `talk:bot:setup <bot-id> <token>` command enables a bot in a specific conversation.

---

## Useful OCC Commands to Know

Here are the key bot management commands:
- `talk:bot:list` — List all installed bots
- `talk:bot:remove <bot-id>` — Remove a bot from specific conversations
- `talk:bot:setup <bot-id> <token>` — Enable a bot in a conversation
- `talk:bot:state <bot-id> <state>` — Change bot state (0=disabled, 1=enabled, 2=no-setup)
- `talk:bot:uninstall <id>` — Completely remove a bot from the server

---

## Step 3: Verify Bot is Enabled

```bash
docker exec -it -u 33 <container_name> /var/www/html/occ talk:bot:list
```

You should see the OpenClaw bot listed with state `1` (enabled).

---

## After That

Once enabled via CLI, go back to the Talk conversation and send a message — the bot should now be active and respond. If your DM policy is `pairing`, you'll need to approve the pairing code as described in the setup instructions.

**References:**

- [Nextcloud Talk Bots & Webhooks Docs](https://nextcloud-talk.readthedocs.io/en/latest/bots/)
- [OCC Commands Reference](https://nextcloud-talk.readthedocs.io/en/latest/occ/)
- [OpenClaw Nextcloud Talk Setup Guide](https://open-claw.me/channels/nextcloud)
