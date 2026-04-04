---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器人不显示为联系人
translated: true
type: note
---

**问：** 在 Nextcloud Talk 中，为什么在对话设置中启用机器人后，该机器人不会显示为联系人或参与者——看起来似乎没有任何变化？

**答：**

这是一个非常常见的困惑点，原因在于 Nextcloud Talk 机器人的根本设计方式。它们的工作原理**与常规用户联系人完全不同**。

---

## 为什么机器人不显示为联系人

### 1. 机器人是 Webhook 监听器，而非用户

Nextcloud Talk 机器人是基于 Webhook 的。当您在对话中启用一个机器人时，每当该房间中发送消息，Nextcloud Talk 就会向机器人注册的 webhook URL 发送 HTTP POST 请求。该机器人并非一个 Nextcloud 用户账户——它没有个人资料、在联系人列表中没有头像，也没有在线状态指示器。它只是一个监听事件的外部服务。

### 2. 启用机器人只是“激活”监听器

当您在对话的机器人设置中点击 **启用**（如您截图所示）时，您是在告诉 Nextcloud Talk：*“对于此对话，开始将消息转发到机器人的 webhook。”* 在 Talk 设置中将机器人添加到频道后，该对话中的每条输入内容都会被发送到 webhook URL。webhook 请求包含重要的安全头部信息 —— `X-Nextcloud-Talk-Signature` 和 `X-Nextcloud-Talk-Random` —— 机器人用它们来验证消息是否合法。

参与列表中不会有任何东西在视觉上“加入”对话。这是设计使然。

### 3. 机器人仅在触发时做出反应

只有当外部 webhook 服务实际响应时，机器人才会看起来有所动作（例如，将消息发送回对话中）。当机器人收到消息时，它会使用共享密钥验证签名，处理消息，然后通过 Talk API 将响应发送回对话。如果机器人的后端服务宕机、配置错误或未在监听——您将完全看不到任何动静，这使得启用机器人看起来像是什么都没发生。

---

## 看起来“什么都没发生”的常见原因

| 原因 | 解释 |
|---|---|
| 机器人后端未运行 | Webhook URL 指向的服务离线或无法访问 |
| Webhook URL 无法访问 | Nextcloud 无法访问该 URL（例如，防火墙、错误的 IP） |
| 签名不匹配 | 机器人因共享密钥错误而拒绝消息 |
| 未满足触发条件 | 某些机器人仅对特定命令做出响应（例如 `@bot hello`） |
| 缺少 AI/Assistant 配置 | 对于像 Assistant Talk Bot 这样的 AI 驱动机器人，Nextcloud Assistant 必须完全配置并正常工作，并且必须为每个房间启用机器人——设置并不简单 |

---

## 启用后您实际应该看到的现象

- 机器人**不会出现**在参与者/联系人列表中
- 机器人**不会显示**为在线状态
- 您只有在机器人**发布消息**到聊天中以响应某个触发器时，才能看到机器人的效果
- 即使用 `@botname` 提及机器人也可能不工作，如果机器人未正确端到端配置

---

## 如何验证机器人是否正常工作

1. 检查机器人指向的外部服务是否正在运行，并且您的 Nextcloud 服务器可以访问
2. 在服务器上运行 `occ talk:bot:list` 命令，以确认机器人已注册并检查其 `error_count`
3. 向机器人应该做出反应的对话发送一条消息
4. 检查 Nextcloud 服务器日志中是否有 webhook 传递错误

---

## 总结

在 Nextcloud Talk 对话设置中启用机器人**与添加联系人或参与者不同**。机器人是一个不可见的 webhook 集成——只有当它主动发布消息响应触发器时才会变得可见。如果您在启用后什么也没看到，问题几乎总是机器人的后端服务无法访问或未正确设置。

**参考文献：**

- [Nextcloud Talk Bots and Webhooks — 官方文档](https://nextcloud-talk.readthedocs.io/en/latest/bots/)
- [Assistant Talk Bot not responding — Nextcloud 社区](https://help.nextcloud.com/t/assistant-talk-bot-not-responding-in-conversation-nextcloud-32-aio/235498/1)
- [Unable to mention bot on Nextcloud Talk — Nextcloud 社区](https://help.nextcloud.com/t/unable-to-mention-bot-on-nextcloud-talk/241841)
- [Nextcloud Custom Bot walkthrough — Raspi Playground](https://koscis.wordpress.com/2025/12/07/nextcloud-custom-bot-part-1/)