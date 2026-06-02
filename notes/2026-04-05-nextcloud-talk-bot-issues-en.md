---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Bot Setup Issues
translated: false
type: note
---

**Full Review — What Happened & What We Learned**

Here's a complete breakdown of the Nextcloud Talk setup process and the issues we hit:

---

## What We Did

### Step 1: Installed the bot via `occ`
```bash
docker exec nextcloud-app-1 php occ talk:bot:install "OpenClaw" "$SECRET" "http://172.17.0.1:8788/nextcloud-talk-webhook" --feature webhook,response,reaction
docker exec nextcloud-app-1 php occ talk:bot:setup 7 eu42ecdy
```

### Step 2: Configured OpenClaw
```json
channels.nextcloud-talk.baseUrl: "http://172.17.0.1:8080"   // was http://localhost:8080
channels.nextcloud-talk.botSecret: "GgLbdQ9i3ifzHKQt3WqgbmJbA94ZX3WDdVXUW0YpaLE="
channels.nextcloud-talk.dmPolicy: "allowlist"
channels.nextcloud-talk.allowFrom: ["*"]
```

---

## Issues We Hit (in order)

### 🔴 Issue 1: Duplicate plugin
- A custom plugin at `~/.openclaw/extensions/nextcloud-talk/` was overriding the bundled one
- **Fix:** Moved it to `.bak`

### 🔴 Issue 2: Wrong baseUrl origin mismatch
- `baseUrl` was `http://localhost:8080` but Nextcloud identifies itself as `http://172.17.0.1:8080` (Docker gateway IP)
- OpenClaw's `isBackendAllowed` check validates the `X-Nextcloud-Talk-Backend` header origin against `baseUrl`
- **Fix:** Changed to `http://172.17.0.1:8080`

### 🔴 Issue 3: Bot secret mismatch
- Installed multiple bots (IDs 3, 4, 5, 6) with different secrets
- OpenClaw was configured with one secret while Nextcloud had another registered
- **Fix:** Fresh install (bot ID 7) with matching secret

### 🟡 Issue 4: No @mention = dropped
- OpenClaw's Nextcloud Talk handler drops messages without an @mention in group rooms
- This is currently the **blocking issue** — the bot IS receiving webhooks (confirmed via test), but all messages are dropped with `drop room eu42ecdy (no mention)`
- The Nextcloud error log shows "Bot error occurred" which is Nextcloud's way of saying the bot didn't respond (because OpenClaw dropped the message silently)

---

## Key Technical Findings

1. **Signature verification works** — HMAC-SHA256(random + body, secret) is correct
2. **Webhook connectivity works** — `http://172.17.0.1:8788` is reachable from Nextcloud container
3. **Messages reach OpenClaw** — confirmed via log showing `nextcloud-talk: drop room eu42ecdy (no mention)`
4. **The mention requirement** — OpenClaw only processes group messages that @mention the bot; this is a design choice that prevents the bot from being spammy in group chats

---

## Current Status

| Component | Status |
|-----------|--------|
| Bot installed in Nextcloud | ✅ ID 7 |
| Bot enabled in room eu42ecdy | ✅ |
| Webhook reachable | ✅ |
| Signature verification | ✅ |
| OpenClaw receives messages | ✅ |
| Messages processed | ❌ Dropped (no @mention) |

---

## What's Still Blocking

The bot needs an **@mention** to respond in group rooms. To use it properly you either:

1. **Use it in a 1:1 DM** — bots work without mentions in direct messages
2. **@mention the bot** in group chat — e.g. `@OpenClaw hello`
3. **Change OpenClaw code** to allow group messages without mention (not recommended for spam prevention)

Want me to change the mention policy, or would you prefer to use the bot in a DM instead?
