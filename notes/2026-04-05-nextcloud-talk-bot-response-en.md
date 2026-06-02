---
audio: false
generated: true
image: false
lang: en
layout: post
title: Test Nextcloud Talk Bot Response
translated: false
type: note
---

**Summary of current status:**

1. ✅ `allowPrivateNetwork: true` — Fix applied, no more "blocked URL" errors
2. ✅ Gateway restarted successfully with new config
3. ✅ Webhook listening at `http://172.17.0.1:8788`
4. ✅ Bot is registered in Nextcloud Talk (id=8, state=1, features=webhook+response)
5. ⚠️ **Nextcloud Talk is NOT sending webhook events** — messages going through polling API instead

**To test if it works now:**

Please **send a new message in the Nextcloud Talk room** (eu42ecdy) and let me know if the bot responds.

If it still doesn't work, the issue is that **Nextcloud Talk 23.0.2 isn't sending webhook events** — this would be a Nextcloud Talk bug or configuration issue, not OpenClaw.

Can you try sending a message now and tell me if you get a response?
