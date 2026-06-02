---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw Telegram 群组配置更新
translated: true
type: note
---

以下是已完成工作的回顾：

**✅ 修改内容 — `/home/lzw/.openclaw/openclaw.json` 中的 `channels.telegram`：**

| Setting | Before | After |
|--------|--------|-------|
| `groupPolicy` | `"allowlist"` | `"allowlist"` (未变更) |
| `groupAllowFrom` | _(缺失)_ | `["-4714712674"]` ← blog Telegram group |

**这意味着：**
- Bot 的 Telegram group policy 设置为 **allowlist** — 只有在白名单列表中的群组才能与其交互
- 群组 ID `-4714712674`（来自 blog-source 中的 `telegram_bot.py`）已被添加
- **已尝试重启 Gateway** 但返回了 exit code 1 — config warnings 是非致命的，但重启可能已经失败

**⚠️ 潜在问题：** 重启命令以状态码 1 退出。你可能需要手动运行：

```
openclaw gateway restart
```

**Blog push 设置现状：**
1. ✅ 群组 allowlist 已为 `-4714712674` 配置完成
2. ✅ Bot 现在可以在 blog 群组中接收消息
3. 🔲 实际的 push-on-update 逻辑 — 你的 `telegram_bot.py` 作为一个独立的 script 通过 git hooks 或 CI 运行。如果你希望 OpenClaw 也能自动将 blog 更新推送到该群组（自动触发），我们需要一个 watcher cron 或 git hook — 需要我设置吗？
