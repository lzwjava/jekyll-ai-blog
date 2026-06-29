---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenRouter API Key Expired Fix
translated: false
type: note
---

The cause is clear:

**Your OpenRouter API key has been invalidated/expired.** The API returned:

```
HTTP 401 — {"error":{"message":"User not found.","code":401}}
```

This means the key stored in `OPENROUTER_API_KEY` no longer exists on OpenRouter's side — it was either revoked, expired, or the account was deleted/recreated.

**Fix it:**
1. Go to https://openrouter.ai/settings/keys
2. Generate a new API key
3. Update your `.env` file:
   ```
   OPENROUTER_API_KEY=***
   ```
4. Either re-source the file (`source .env`) or restart the shell, then retry `ww note`.

The proxy (`HTTP_PROXY=http://127.0.0.1:7890`) is working fine — requests go through and responses come back. The 401 is purely an auth issue on the key itself.