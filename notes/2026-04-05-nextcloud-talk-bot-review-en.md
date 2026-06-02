---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Bot Configuration Review
translated: false
type: note
---

## Comprehensive Review — Nextcloud Talk Bot Configuration

### ✅ What's Fixed

| Item | Before | After |
|------|--------|-------|
| `baseUrl` | `http://172.17.0.1:8080` | `http://localhost` ✅ |
| `webhookPublicUrl` | (missing) | `http://172.17.0.1:8788` ✅ |
| `allowPrivateNetwork` | (missing) | `true` ✅ |
| Bot ID | 8 (broken) | 9 (fresh install) ✅ |
| Bot error_count | 40+ errors | 0 ✅ |

### ✅ Current Configuration

```
Nextcloud config.php:
  overwrite.cli.url = "http://localhost"
  → Sent in X-Nextcloud-Talk-Backend header

OpenClaw nextcloud-talk config:
  baseUrl: "http://localhost"        ← Matches header ✅
  webhookPublicUrl: "http://172.17.0.1:8788"  ← Where Nextcloud calls
  botSecret: [hidden]
  allowPrivateNetwork: true           ← Allows Docker IPs ✅
  rooms.eu42ecdy.requireMention: false

Bot Registration:
  ID: 9, State: 1, Features: webhook, response, reaction
  Enabled in: eu42ecdy, 7df4dtc5
```

### ⚠️ One Issue Found in Logs

The old logs (BEFORE reinstall at ~02:49 HKT) show:
```
nextcloud-talk: drop room 7df4dtc5 (not allowlisted)
nextcloud-talk final reply failed: room not found
```

This was caused by the old bot (ID 8) trying to use rooms that were deleted. **This is resolved now** — the new bot (ID 9) was installed fresh.

### 🚀 Test Required

**Please send a message NOW** in the Nextcloud Talk room. Since the reinstall (~02:49 HKT), there have been:
- ✅ No errors in Nextcloud error log
- ✅ Bot error_count = 0

If you send a message and it works, we're done! 🦞
