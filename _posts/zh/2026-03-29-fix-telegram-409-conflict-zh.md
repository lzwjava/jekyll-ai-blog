---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Telegram Bot Token 409 冲突
translated: true
type: note
---

以下是审核结果 — 发现了 **两个不同的问题**：

---

**问题 1: `getUpdates` 409 Conflict (🔴 严重)**
Telegram bot token 正在被 **两个程序同时使用**：

- OpenClaw 的 Telegram plugin (long polling)
- 你 blog-source 中的 `telegram_bot.py` (同样在调用 `getUpdates`)

它们在争夺同一个 polling 连接 → 导致 OpenClaw 不断收到 `409 Conflict` 错误并停滞。

**问题 2: Group config 已修复 ✅**
`channels.telegram.groups` 的配置方式生效了 — 最近的 logs 中不再出现 "Invalid allowFrom" 错误。Group "blog" 现在已被识别。

---

**要修复 409 conflict**，你需要 **停止 `telegram_bot.py` 的 polling**。由于 OpenClaw 现在负责处理向 Group 发送 push messages，你现有的 push script 应该只在需要时运行（例如由 git hook 触发），而不是作为一个持续运行的 poller。

最简单的修复方法 — 在你的 `telegram_bot.py` 中，注释掉或删除调用 `getUpdates` 的 `get_chat_id` 任务，因为你已经获取了 chat ID，且 OpenClaw 现在占用了该 Telegram 连接：

```python
# 注释掉或删除 getUpdates polling 部分：
# def get_chat_id(bot_token):
#     url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
#     ...
```

需要我帮你进行这项修改吗？
