---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Telegram Group ID Config Error
translated: false
type: note
---

The key was reading the **error log**, which told me exactly what to do:

```
Invalid allowFrom entry: "-4714712674"
- allowFrom/groupAllowFrom authorization expects numeric Telegram sender user IDs only.
- To allow a Telegram group or supergroup, add its negative chat ID under
  "channels.telegram.groups" instead.
```

**What I did — two changes to `openclaw.json`:**

**Before (wrong):**

```json
"channels": {
  "telegram": {
    "groupPolicy": "allowlist",
    "groupAllowFrom": ["-4714712674"]   // ❌ user IDs only
  }
}
```

**After (correct):**

```json
"channels": {
  "telegram": {
    "groupPolicy": "allowlist",
    "groupAllowFrom": [],               // ✅ empty - user auth not needed
    "groups": {
      "-4714712674": {                  // ✅ group chat IDs here
        "requireMention": true
      }
    }
  }
}
```

**The distinction:**

- `groupAllowFrom` → for **individual user IDs** (who can trigger the bot)
- `groups` → for **group chat IDs** (which groups are allowed)

So the chat ID `-4714712674` went from being incorrectly treated as a user identifier, to being properly recognized as a group chat.
