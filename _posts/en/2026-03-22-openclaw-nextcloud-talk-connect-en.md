---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting OpenClaw to Nextcloud Talk
translated: false
type: note
---

Here's how to wire it up:

### Step 1: Install the plugin

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

### Step 2: Create a bot on your Nextcloud server

```bash
docker exec nextcloud-app-1 php occ talk:bot:install "OpenClaw" "your-shared-secret" "http://<your-server-ip>:8788/nextcloud-talk-webhook" --feature reaction
```

Replace `your-shared-secret` with something strong, and `<your-server-ip>` with your server's actual IP/hostname (the one your Gateway runs on).

### Step 3: Configure OpenClaw

```bash
openclaw config set channels.nextcloud-talk.enabled true
openclaw config set channels.nextcloud-talk.baseUrl "http://localhost:8080"
openclaw config set channels.nextcloud-talk.botSecret "your-shared-secret"
```

If your Gateway is behind a reverse proxy, also set:

```bash
openclaw config set channels.nextcloud-talk.webhookPublicUrl "https://your-public-domain/nextcloud-talk-webhook"
```

### Step 4: Restart and test

```bash
openclaw gateway restart
```

Then in Nextcloud Talk, open the room you want to use, go to **Room Settings → Bots**, and enable the "OpenClaw" bot. Send it a message and it should reply.

Want me to run any of these steps for you?