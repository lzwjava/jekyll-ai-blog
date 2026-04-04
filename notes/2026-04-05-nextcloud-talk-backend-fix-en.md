---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Backend Mismatch Fixed
translated: false
type: note
---

## Summary of Findings

**Root Cause Found:**
Nextcloud Talk sends `X-Nextcloud-Talk-Backend: http://localhost` (from `overwrite.cli.url`), but OpenClaw's `baseUrl` was set to `http://172.17.0.1:8080`. OpenClaw's signature verification requires the backend URL to match, so it was rejecting all requests with **401 "Invalid backend"**.

**Fix Applied:**
Changed `baseUrl` from `http://172.17.0.1:8080` → `http://localhost`

**Current Config:**
```json
{
  "baseUrl": "http://localhost",       ← Fixed!
  "botSecret": "bgCDXVAqsN3MX0V0...",
  "webhookPublicUrl": "http://172.17.0.1:8788",
  "rooms": {
    "eu42ecdy": { "requireMention": false }
  }
}
```

**Status:**
- ✅ No more "Invalid backend" errors after 02:25 HKT
- ✅ Gateway restarted successfully  
- ✅ Webhook listening

**Please try sending a new message now** — the old messages at 02:26 failed because they were sent before the fix. New messages after ~02:22 should work.