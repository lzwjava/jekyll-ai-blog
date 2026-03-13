---
audio: false
generated: true
image: false
lang: en
layout: post
title: Approve OpenClaw Pairing Codes
translated: false
type: note
---

Question: How do I approve a pairing code from a bot using `openclaw pairing approve` as the bot owner in OpenClaw?

Answer:

## How OpenClaw Pairing Works

Pairing is OpenClaw's way of controlling who can issue commands to your agent. When an unknown user DMs your bot, they get an 8-character code, and you — the bot owner — run `openclaw pairing approve <channel> <CODE>` to activate them. Codes expire after one hour.

---

## Full Step-by-Step: Approving a Pairing Code

### Step 1 — User sends a DM to your bot

The user messages your bot (e.g., on Telegram, Discord, WhatsApp, etc.). Since they are unknown, the bot does not process their message — it replies with an 8-character pairing code (uppercase letters, excluding ambiguous characters like 0, O, 1, and I).

---

### Step 2 — User shares the code with you

The user must tell you (the bot owner) what their pairing code is — for example: `JN4MSY23`

---

### Step 3 — Check pending pairing requests (optional)

On your Linux server, run:

```bash
openclaw pairing list telegram
```

Replace `telegram` with your channel: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`

---

### Step 4 — Approve the pairing code

```bash
openclaw pairing approve <channel> <CODE>
```

**Examples by platform:**

```bash
# Telegram
openclaw pairing approve telegram JN4MSY23

# Discord
openclaw pairing approve discord JN4MSY23

# WhatsApp
openclaw pairing approve whatsapp JN4MSY23

# Slack
openclaw pairing approve slack JN4MSY23

# Signal
openclaw pairing approve signal JN4MSY23

# LINE
openclaw pairing approve line JN4MSY23
```

You should see a confirmation: `Approved telegram sender <user-id>`

---

### If Running in Docker

Enter the container first, then run the approve command:

```bash
# SSH into your server
ssh root@YOUR_SERVER_IP

# Enter the OpenClaw container
docker exec -it openclaw-mupw-openclaw-1 sh

# Approve the pairing code
openclaw pairing approve telegram ABCD1234

# Exit container
exit

# Restart the container
docker restart openclaw-mupw-openclaw-1
```

---

### If Running Docker Compose

Run the approve command directly via Docker Compose from the folder containing your `docker-compose.yml`:

```bash
docker compose run --rm openclaw-cli pairing approve telegram <CODE>
```

---

### Via Web UI (Dashboard Chat Box)

In the OpenClaw web interface chat box, type:

```
openclaw pairing approve telegram <CODE>
```

---

## Important Notes

| Topic | Details |
|---|---|
| Code expiry | Codes expire after **1 hour** — if missed, the user must send another message to get a new code |
| Max pending codes | Pending DM pairing requests are capped at 3 per channel by default; additional requests are ignored until one expires or is approved |
| After approval | The user is added to a local allowlist and can now interact with the bot normally |
| Approve all pending | `openclaw pairing approve telegram` (no code = approve all pending) |

---

## Permanent Authorization (Recommended for Production)

After approving via pairing code, switch to **allowlist mode** so the user never needs to re-pair:

```bash
# Set dmPolicy to allowlist and add user's Telegram numeric ID
openclaw config set channels.telegram.dmPolicy allowlist
openclaw config set channels.telegram.allowFrom '["123456789"]'
openclaw restart
```

Telegram needs numeric IDs, not @usernames. WhatsApp needs E.164 format like `+15551234567`. Discord needs the full numeric user ID.

References:

- [OpenClaw Pairing Docs (official)](https://docs.openclaw.ai/channels/pairing)
- [OpenClaw Pairing Explained - Stack Junkie](https://www.stack-junkie.com/blog/openclaw-pairing-explained)
- [Connect Telegram to OpenClaw on VPS - Medium](https://medium.com/@mikhela65/how-to-connect-telegram-to-openclaw-on-hostinger-vps-control-your-ai-agent-from-anywhere-532ab7003d0e)
- [Running OpenClaw in Docker - Simon Willison](https://til.simonwillison.net/llms/openclaw-docker)
- [OpenClaw Pairing Docs - LearnClawdbot](https://www.learnclawdbot.org/docs/start/pairing)
- [OpenClaw GitHub README](https://github.com/openclaw/openclaw/blob/main/README.md)