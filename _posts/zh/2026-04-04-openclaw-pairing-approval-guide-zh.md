---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw配对与批准指南
translated: true
type: note
---

好问题，老板。以下是详细说明：

## `openclaw pairing approve` 的工作原理

当未知的 Telegram 用户向您的机器人发送消息，且频道配置了 `dm.policy: "pairing"` 时，OpenClaw 会：

1. **生成一个短代码**（8位字符，大写字母，排除易混淆字符如 `0O1I`）
2. **将代码发送给发送者**作为回复："您的配对码是 X2SKVW4Y..."
3. **创建一个待处理请求**，存储在 `~/.openclaw/credentials/telegram-pairing.json` 中
4. **阻止他们的消息**——在批准之前，消息不会得到处理
5. 代码**在 1 小时后过期**

当您运行 `openclaw pairing approve telegram X2SKVW4Y` 时，CLI 会：
- 在待处理请求文件中查找该代码
- 将发送者的 Telegram 用户 ID (`610574272`) 移至**允许列表**文件：`~/.openclaw/credentials/telegram-allowFrom.json`
- 来自该用户 ID 的后续消息现在将被信任并直接通过

## “所有者”的含义

这里没有魔法般的身份验证。**“所有者”仅指具有服务器 shell 访问权限**且能运行 `openclaw pairing approve` 命令的人。配对文档指出：

> *“拥有 OpenClaw Gateway 配置和 CLI 访问权限并控制其的人员被视为所有者，并负责批准这些配对请求。”*

这是一个**信任边界**——如果您能 SSH 进入服务器并运行 CLI 命令，您就是所有者。系统不会检查外部身份；它只信任能够执行批准命令的人。

## 为什么您的代码总在过期

代码有效期为 1 小时，但真正的症结在于时间——配对消息出现在您的聊天中，当您将其转达给我时，待处理请求可能已经轮换（机器人对每个发送者大约每小时重新生成一次代码）。待处理请求也限制为**每个频道 3 个**。

**解决方案：**
- 直接从服务器的 CLI 进行批准（比通过我转达更快）
- 或者，如果您设置了监视器或 cron，我可以尝试自动批准来自您用户 ID `610574272` 的 Telegram 配对请求

需要我尝试什么具体方案吗？