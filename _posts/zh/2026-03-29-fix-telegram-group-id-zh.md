---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Telegram 群组 ID 配置错误
translated: true
type: note
---

关键在于阅读 **error log**，它准确地告诉我该怎么做：

```
Invalid allowFrom entry: "-4714712674"
- allowFrom/groupAllowFrom authorization expects numeric Telegram sender user IDs only.
- To allow a Telegram group or supergroup, add its negative chat ID under 
  "channels.telegram.groups" instead.
```

**我所做的操作 —— 对 `openclaw.json` 进行了两处修改：**

**修改前（错误）：**
```json
"channels": {
  "telegram": {
    "groupPolicy": "allowlist",
    "groupAllowFrom": ["-4714712674"]   // ❌ 仅限 user IDs
  }
}
```

**修改后（正确）：**
```json
"channels": {
  "telegram": {
    "groupPolicy": "allowlist",
    "groupAllowFrom": [],               // ✅ 为空 - 不需要 user auth
    "groups": {
      "-4714712674": {                  // ✅ group chat IDs 放在这里
        "requireMention": true
      }
    }
  }
}
```

**区别在于：**
- `groupAllowFrom` → 用于 **individual user IDs**（谁可以触发 bot）
- `groups` → 用于 **group chat IDs**（允许哪些群组）

因此，chat ID `-4714712674` 从之前被错误地当作 user identifier，变为了被正确识别为 group chat。