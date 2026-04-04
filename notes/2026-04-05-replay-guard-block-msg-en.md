---
audio: false
generated: true
image: false
lang: en
layout: post
title: Replay Guard Blocks Duplicate Messages
translated: false
type: note
---

I found the issue. Here's what's happening:

**Problem Analysis:**

1. **Your `requireMention: false` config IS correct** — it's at `rooms.eu42ecdy.requireMention`, which is the right place.

2. **The real issue: Replay Guard deduplication**
   - The dedupe file shows: `{"eu42ecdy:1": 1775323541972}`
   - This means messages with `messageId=1` from room `eu42ecdy` are being blocked as duplicates for 24 hours (TTL = 86400000ms)
   - Every message with `messageId=1` after the first is rejected **BEFORE** the mention check even runs

3. **Flow:** `shouldProcessMessage (replay check)` → if passed → `handleNextcloudTalkInbound` → mention gate check

The replay guard runs FIRST, so even with `requireMention: false` correctly set, duplicate message IDs get blocked before reaching the mention logic.

**Likely cause:** Nextcloud Talk is sending the same `messageId` for all messages (or you're resending the same test webhook).

**Fix options:**

1. **Quick fix — clear the replay dedupe file:**
   ```bash
   rm /home/lzw/.openclaw/nextcloud-talk/replay-dedupe/*.json
   echo '{}' > /home/lzw/.openclaw/nextcloud-talk/replay-dedupe/*.json
   ```
   Then send a new message with a unique ID.

2. **Or restart the gateway** to pick up the config fresh.

3. **Check Nextcloud Talk** — ensure it's generating unique message IDs for each message, not reusing `1`.

Want me to clear the dedupe file and verify the config?