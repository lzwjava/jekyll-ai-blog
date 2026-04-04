---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three-Layer Configuration Alignment Problem
translated: false
type: note
---

## Expanded: The Three-Layer Configuration Problem

### Where Configuration Lives

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONFIG LOCATION #1: Nextcloud config.php                               │
│  File: /path/to/nextcloud/config/config.php                            │
│  Key:   'overwrite.cli.url'                                           │
│  Purpose: What Nextcloud tells bots about itself                        │
│  Value: 'http://localhost:8080'                                         │
│  Used by: Nextcloud when sending X-Nextcloud-Talk-Backend header        │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                        This value goes into the header
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  CONFIG LOCATION #2: OpenClaw openclaw.json                            │
│  File: ~/.openclaw/openclaw.json                                        │
│  Keys:  baseUrl, webhookPublicUrl, botSecret, rooms[].requireMention    │
│  Purpose: How OpenClaw validates and responds to Nextcloud              │
│                                                                         
│  baseUrl = "http://localhost:8080"                                      │
│    ↑ Must match X-Nextcloud-Talk-Backend header exactly                │
│    ↓ Used for BOTH incoming signature validation AND outgoing API calls  │
│                                                                         
│  webhookPublicUrl = "http://172.17.0.1:8788"                           │
│    ↑ Where Nextcloud should send webhooks (must be reachable from       │
│      inside Docker network)                                             │
│                                                                         
│  botSecret = "bgCDXVAqsN3MX..."                                        │
│    ↑ Shared secret for HMAC signature (must match bot registration)     │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                        When OpenClaw replies, it calls this URL
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  CONFIG LOCATION #3: Nextcloud Database (oc_talk_bots_server)          │
│  Table: oc_talk_bots_server                                            │
│  Columns: id, name, url, url_hash, secret, features, state               │
│  Purpose: Nextcloud's internal record of registered bots                 │
│                                                                         
│  url = "http://172.17.0.1:8788/nextcloud-talk-webhook"                 │
│    ↑ The webhook URL Nextcloud calls when messages arrive               │
│    ↑ Must match OpenClaw's webhookPublicUrl                            │
│                                                                         
│  secret = "bgCDXVAqsN3MX..."                                           │
│    ↑ Must match OpenClaw's botSecret                                   │
│    ↑ Used by Nextcloud to sign outgoing webhooks                        │
│    ↑ Used by OpenClaw to verify incoming signatures                     │
│                                                                         
│  Table: oc_talk_bots_conversation                                      │
│  Columns: id, bot_id, token, state                                     │
│  Purpose: Which rooms the bot is enabled in                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### The Alignment Matrix

| Setting | config.php | openclaw.json | Database | Must Match |
|---------|------------|---------------|----------|------------|
| Nextcloud internal URL | `http://localhost:8080` | `baseUrl` | - | ✅ All 3 |
| Webhook URL (public) | - | `webhookPublicUrl` | `url` column | ✅ Both |
| Shared secret | - | `botSecret` | `secret` column | ✅ Both |
| Room enablement | - | `rooms.eu42ecdy` | `oc_talk_bots_conversation` | ✅ Both |

**If ANY of these don't align, things break silently.**

---

### Signature Verification vs API Call: The Silent Mismatch

This was the most confusing part. Here's why:

#### What "Signature Verification" Means

```
┌──────────────────────────────────────────────────────────────────┐
│  NEXTcloud sends webhook to OpenClaw                              │
│                                                                   │
│  Headers:                                                         │
│    X-Nextcloud-Talk-Backend: http://localhost:8080               │
│    X-Nextcloud-Talk-Random: <random-64-chars>                    │
│    X-Nextcloud-Talk-Signature: <hmac-sha256>                      │
│                                                                   │
│  Body:                                                            │
│    {"type":"Activity", "actor":{...}, "object":{...}, ...}       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
                   OpenClaw verifies the signature
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Signature = HMAC-SHA256(                                         │
│    Random + Body,    ←  concatenated                               │
│    BotSecret         ←  shared secret                              │
│  )                                                                 │
│                                                                   │
│  OpenClaw computes this using its botSecret                        │
│  Compares to X-Nextcloud-Talk-Signature header                    │
│  If match → request is authentic ✅                               │
│  If no match → 401 Invalid signature ❌                           │
└──────────────────────────────────────────────────────────────────┘
```

**This verification uses `baseUrl` to check the `X-Nextcloud-Talk-Backend` header.**

---

#### What "API Call" Means

```
┌──────────────────────────────────────────────────────────────────┐
│  OPENCLAW sends reply back to Nextcloud                           │
│                                                                   │
│  OpenClaw calls:                                                  │
│    POST http://localhost:8080/ocs/v2.php/apps/spreed/...         │
│                 ↑                                                 │
│                 baseUrl used here too!                            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
                   Nextcloud receives the API call
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  If baseUrl = "http://localhost" (without port):                  │
│    Nextcloud is NOT listening on port 80                          │
│    nginx is on port 80 → returns 404                              │
│    OpenClaw sees: "room not found (token=eu42ecdy)"              │
│                                                                   │
│  If baseUrl = "http://localhost:8080":                           │
│    Nextcloud IS listening on port 8080                           │
│    Returns proper response ✅                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

### Why It Looked Like "Signature Verification Passed But API Call Failed"

```
NEXT CLOUD LOG (what Nextcloud reports to us):
┌─────────────────────────────────────────────────────────────┐
│  POST http://172.17.0.1:8788/nextcloud-talk-webhook        │
│  ← This is the webhook delivery to OpenClaw                │
│                                                             │
│  Result: 401 Invalid backend                                │
│  ← OpenClaw rejected it because baseUrl didn't match        │
│                                                             │
│  BUT: Nextcloud doesn't know WHY it failed                 │
│  It just sees the final 401                                 │
└─────────────────────────────────────────────────────────────┘

OPENCLAW LOG (what OpenClaw reports to us):
┌─────────────────────────────────────────────────────────────┐
│  Received webhook from Nextcloud                            │
│  Signature check... FAILED (401 Invalid backend)            │
│  ← This blocked us from seeing the actual payload          │
│                                                             │
│  Later, after baseUrl fix:                                  │
│  Received webhook (OK)                                      │
│  Attempting to send reply to http://localhost/ocs/...      │
│  ← But we never logged WHAT that URL resolved to            │
│                                                             │
│  Response: 404                                              │
│  We log: "room not found (token=eu42ecdy)"                 │
│  ← This error message doesn't tell us the URL was wrong!    │
└─────────────────────────────────────────────────────────────┘
```

**The silent failure:** OpenClaw's error message said "room not found" but the REAL issue was "I tried to call `http://localhost/ocs/v2.php/...` which hit nginx (port 80) instead of Nextcloud (port 8080)."

---

### The Three Silent Failures

| Failure Point | What We Expected | What Actually Happened | Error Message |
|---------------|------------------|------------------------|---------------|
| **Signature** | `baseUrl` matches header | `baseUrl` was `http://172.17.0.1:8080`, header was `http://localhost` | `401 Invalid backend` |
| **Payload Parse** | `type` is "Create" | Nextcloud sends `type: "Activity"` | `400 Invalid payload format` |
| **API Call** | `http://localhost:8080` works | `http://localhost` (port 80) → nginx → 404 | `room not found` |

Each failure hid behind the previous one because:
1. Signature rejection = payload never parsed
2. Payload rejection = API never called
3. API 404 = looked like a room problem, not a URL problem

---

### The Port 80 vs Port 8080 Confusion

```
┌────────────────────────────────────────────────────────────────┐
│  YOUR LAPTOP (where you're accessing things from)              │
│                                                                 │
│  Port 80:   nginx reverse proxy (handles https://yourdomain.com)│
│  Port 8080: Nextcloud Apache inside Docker                      │
│                                                                 │
│  When OpenClaw calls "http://localhost:8080" from the HOST:    │
│    localhost = host machine                                     │
│    :8080 = Docker port mapping → reaches Nextcloud ✅           │
│                                                                 │
│  When OpenClaw calls "http://localhost" (no port):             │
│    localhost = host machine                                     │
│    (default port 80) → reaches nginx ❌                         │
│    nginx doesn't know /ocs/v2.php/... → 404                    │
└────────────────────────────────────────────────────────────────┘
```

**This is why `http://localhost` works for signature verification (Nextcloud sends it, OpenClaw compares it) but fails for API calls (OpenClaw uses it to make calls, hits wrong service).** 🦞