---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Bot Configuration in OpenClaw
translated: false
type: note
---

Question: How do I set up Nextcloud Talk in OpenClaw (AI agent), and why can't I add the bot to a room?

Answer:

## Setting Up Nextcloud Talk in OpenClaw

Nextcloud Talk is supported in OpenClaw via a plugin (webhook bot). It supports direct messages, rooms, reactions, and markdown messages. It is **not** bundled with the core install — you must install it separately.

---

### Step 1: Install the Nextcloud Talk Plugin

Install via CLI from the npm registry:

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Or if running from a local git checkout:

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

---

### Step 2: Register the Bot on Your Nextcloud Server

SSH into your Nextcloud server and run the OCC command:

```bash
./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
```

Replace `<shared-secret>` with a strong 40+ character secret, and `<webhook-url>` with the Gateway's publicly accessible webhook endpoint (e.g., `https://gateway.example.com:8788`).

---

### Step 3: Enable the Bot in the Room

Go to your target room settings in Nextcloud and **enable the bot** you just created.

This is a required manual step and is the most common reason bots cannot be added to a room — **you must explicitly enable the bot per room** inside Nextcloud Talk's room settings.

---

### Step 4: Configure OpenClaw

Update your OpenClaw config file with the following minimal configuration:

```json
{
  "channels": {
    "nextcloud-talk": {
      "enabled": true,
      "baseUrl": "https://cloud.example.com",
      "botSecret": "shared-secret",
      "dmPolicy": "pairing"
    }
  }
}
```

Then restart the gateway to apply the changes.

---

### Why Can't You Add the Bot to a Room? (Common Issues)

**1. You forgot to enable the bot in Room Settings.**
After installing via OCC, the bot still needs to be manually enabled in each Talk room where you want it available.

**2. Webhook not reachable.**
Your Nextcloud server must be able to send data to the OpenClaw Gateway. If you are behind a reverse proxy, ensure you set `webhookPublicUrl` in your config.

**3. DMs treated as rooms.**
The standard webhook payload does not distinguish between DMs and room messages. To fix this, provide `apiUser` and `apiPassword` so the plugin can perform room-type lookups.

**4. Room allowlist / groupPolicy blocking the bot.**

By default, `groupPolicy` is set to `"allowlist"` (mention-gated). You must explicitly allowlist rooms like this:

```json
{
  "channels": {
    "nextcloud-talk": {
      "rooms": {
        "room-token": { "requireMention": true }
      }
    }
  }
}
```

To allow no rooms, keep the allowlist empty or set `groupPolicy: "disabled"`.

---

### DM Pairing Flow

By default, OpenClaw uses a "pairing" model for direct messages. When someone messages the bot for the first time, they get a pairing code. An administrator then approves it:

```bash
openclaw pairing list nextcloud-talk
openclaw pairing approve nextcloud-talk <CODE>
```

For wider deployments, you can switch to open policy:

```json
"dmPolicy": "open",
"allowFrom": ["*"]
```

---

### Known Limitations

- **No thread support** — every bot response goes to the main conversation.
- **Media is URL-only** — the bot cannot upload files directly; it sends URL links instead.
- **Bots cannot initiate DMs** — the user must message the bot first to establish the connection.

References:

- [OpenClaw Nextcloud Talk Official Docs](https://docs.openclaw.ai/channels/nextcloud-talk)
- [Connecting OpenClaw AI Agents to Nextcloud Talk – Team 400 Blog](https://team400.ai/blog/2026-04-openclaw-nextcloud-talk-ai-agents)
- [OpenClaw Nextcloud Talk Setup Guide](https://open-claw.me/channels/nextcloud)
- [OpenClaw GitHub README](https://github.com/openclaw/openclaw/blob/main/README.md)
- [Claw Docs – Nextcloud Talk](https://docs.claw.so/engine/channels/nextcloud-talk/)
