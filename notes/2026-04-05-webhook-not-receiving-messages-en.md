---
audio: false
generated: true
image: false
lang: en
layout: post
title: Webhook not receiving messages after restart
translated: false
type: note
---

**Summary of current state:**

1. ✅ Config correct: `requireMention: false` for room `eu42ecdy`
2. ✅ Gateway running 
3. ✅ Webhook listening on `http://localhost:8788/nextcloud-talk-webhook`
4. ✅ Dedupe files cleared (empty `{}`)
5. ❌ **No new webhook messages received after restart** (only my own commands in logs)

**The issue:** The gateway isn't receiving any new messages from Nextcloud Talk after the restart.

**Questions:**

1. **Did you send a NEW message** from Nextcloud Talk **AFTER** the restart (after 02:03 AM)?
2. Or are you looking at the same old message that was blocked earlier?

If you did send a new message and it's still not working, the problem might be:

- **Nextcloud Talk sending duplicate messageId=1** — every message has the same ID, so the first one after restart would be processed, but any subsequent message with ID=1 would be blocked by replay guard (because the first one would be recorded in dedupe)

Can you check in Nextcloud Talk what message ID it's sending? Or try sending a message RIGHT NOW while I watch the logs in real-time?