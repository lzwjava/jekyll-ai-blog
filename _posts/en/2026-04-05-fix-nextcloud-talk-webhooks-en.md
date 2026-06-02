---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Nextcloud Talk Bot Webhooks in Docker
translated: false
type: note
---

Question: How do I correctly fix Nextcloud Talk bot/webhook configuration inside Docker, especially when the network is complex with a proxy, and the `X-Nextcloud-Talk-Backend` header causes "Invalid backend" (401) errors?

Answer:

## Root Cause Explained

When Nextcloud Talk sends a webhook to your bot, it includes an `X-Nextcloud-Talk-Backend` header. The value in this header is derived directly from `overwrite.cli.url` in your `config.php`. Your bot framework (OpenClaw) uses this header to verify that the request is coming from a trusted Nextcloud backend — if its configured `baseUrl` doesn't match what's in the header, it rejects the request with **401 "Invalid backend"**.

In Docker environments this becomes confusing because:
- Nextcloud's `overwrite.cli.url` may be set to `http://localhost` (for CLI/cron use)
- Your bot's `baseUrl` may be set to a Docker gateway IP like `http://172.17.0.1:8080`
- These two values don't match → every webhook call is rejected

---

## The Full Fix Checklist

### 1. Align `baseUrl` with `overwrite.cli.url`

The single most important fix. Your bot's `baseUrl` **must exactly match** what Nextcloud puts in `X-Nextcloud-Talk-Backend`.

Check what Nextcloud sends:
```bash
# Check your Nextcloud config.php inside the container
docker exec -it <nextcloud_container> cat /var/www/html/config/config.php | grep overwrite
```

Then set your bot config to match exactly:
```json
{
  "baseUrl": "http://localhost",
  "botSecret": "your_secret_here",
  "webhookPublicUrl": "http://172.17.0.1:8788"
}
```

> ⚠️ `baseUrl` = what Nextcloud **thinks it is** (from `overwrite.cli.url`)
> ⚠️ `webhookPublicUrl` = where your bot is **actually reachable** from Nextcloud's perspective

---

### 2. Install the Bot with the Right Webhook URL

The webhook URL passed to `occ talk:bot:install` must be the address that **Nextcloud can actually reach your bot on** — not `localhost` from the bot's perspective, but the Docker host gateway or container IP:

```bash
# Run inside Nextcloud container
docker exec -it -u 33 <nextcloud_container> \
  /var/www/html/occ talk:bot:install \
  "MyBot" \
  "<64-128 char secret>" \
  "http://172.17.0.1:8788/nextcloud-talk-webhook" \
  --feature webhook --feature response --feature reaction
```

Replace `172.17.0.1` with the actual Docker host IP (the default bridge gateway). Verify it:
```bash
docker network inspect bridge | grep Gateway
```

---

### 3. Verify `overwrite.cli.url` is Set Correctly

In `config.php`, this should be the URL Nextcloud uses for internal/CLI operations:

```php
'overwrite.cli.url' => 'http://localhost',
```

Or if behind a real domain/reverse proxy, set it to the public URL:
```php
'overwrite.cli.url' => 'https://cloud.yourdomain.com',
```

Then your bot's `baseUrl` must match that same value.

---

### 4. Network Reachability — The Docker Networking Problem

In Docker environments with proxies, there are **two separate reachability problems**:

| Direction | From | To | Common Problem |
|---|---|---|---|
| Nextcloud → Bot (webhook delivery) | Nextcloud container | Bot process | Bot not accessible via Docker host IP |
| Bot → Nextcloud (sending replies) | Bot process | Nextcloud container | Bot uses wrong Nextcloud URL |

**Fix for Nextcloud → Bot:**
- Make sure your bot is listening on `0.0.0.0`, not `127.0.0.1`
- Ensure port is exposed or the containers share a Docker network
- If using a proxy that intercepts outbound traffic from Nextcloud, whitelist the bot's webhook IP/port

**Fix for Bot → Nextcloud:**
- The bot must call Nextcloud at its real internal address (container name, host IP, or `localhost` depending on setup)
- If Nextcloud is behind a reverse proxy with TLS, the bot may need to use the public HTTPS URL instead of internal HTTP

---

### 5. If Using a Proxy (e.g., Clash, V2Ray, etc.)

If the Docker host has a transparent proxy for outbound traffic:

```bash
# Check if the proxy intercepts Docker-internal traffic
# In Nextcloud container:
curl -v http://172.17.0.1:8788/nextcloud-talk-webhook
```

You may need to **exclude Docker internal subnets** from the proxy. For example in Clash:
```yaml
bypass:
  - 172.16.0.0/12
  - 192.168.0.0/16
  - 10.0.0.0/8
```

---

### 6. Verify Signature Verification Is Working

Nextcloud Talk signs webhook requests using HMAC-SHA256 over the `X-Nextcloud-Talk-Random` header value concatenated with the request body, using the shared secret. Your bot must verify this signature — and it also uses the same method when sending replies back.

Test the signature manually:
```bash
# Simulate what Nextcloud sends to your bot
RANDOM_HEADER=$(openssl rand -hex 32)
BODY='{"test": "message"}'
SECRET="your_bot_secret"
SIG=$(echo -n "${RANDOM_HEADER}${BODY}" | openssl dgst -sha256 -hmac "${SECRET}" | cut -d' ' -f2)

curl -X POST http://localhost:8788/nextcloud-talk-webhook \
  -H "Content-Type: application/json" \
  -H "X-Nextcloud-Talk-Random: $RANDOM_HEADER" \
  -H "X-Nextcloud-Talk-Signature: $SIG" \
  -H "X-Nextcloud-Talk-Backend: http://localhost" \
  -d "$BODY"
```

---

### 7. Re-register the Bot After Config Changes

After fixing the config, always remove and reinstall the bot to clear stale state:

```bash
# List bots
docker exec -it -u 33 <nextcloud_container> /var/www/html/occ talk:bot:list

# Remove old bot (use the ID from list)
docker exec -it -u 33 <nextcloud_container> /var/www/html/occ talk:bot:remove <bot_id>

# Reinstall with correct webhook URL
docker exec -it -u 33 <nextcloud_container> \
  /var/www/html/occ talk:bot:install \
  "MyBot" "<secret>" "http://172.17.0.1:8788/webhook" \
  --feature webhook --feature response --feature reaction
```

---

### Summary of All Values and What They Mean

```
config.php → overwrite.cli.url = "http://localhost"
                    ↓ (Nextcloud puts this in X-Nextcloud-Talk-Backend header)

Bot config → baseUrl = "http://localhost"   ← Must match exactly!
Bot config → webhookPublicUrl = "http://172.17.0.1:8788"  ← Where bot is reachable

occ talk:bot:install URL = "http://172.17.0.1:8788/webhook"  ← Same as webhookPublicUrl
```

References:

- [Nextcloud Talk Bots & Webhooks Developer Documentation](https://nextcloud-talk.readthedocs.io/en/latest/bots/)
- [OpenClaw GitHub Issue #6174 - Bot replies fail with 401](https://github.com/openclaw/openclaw/issues/6174)
- [Nextcloud Community - overwrite.cli.url discussion](https://help.nextcloud.com/t/question-what-is-the-correct-setting-for-overwrite-cli-url/228997)
- [Nextcloud Talk HPB with Docker - Arno Welzel](https://arnowelzel.de/en/nextcloud-talk-high-performance-backend-with-docker)
