---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批准 OpenClaw 配对代码
translated: true
type: note
---

问题：在 OpenClaw 中，作为 bot 所有者，如何使用 `openclaw pairing approve` 批准来自 bot 的 pairing code？

答案：

## OpenClaw Pairing 如何工作

Pairing 是 OpenClaw 控制谁可以向您的 agent 发出命令的方式。当未知用户向您的 bot 发送 DM 时，他们会得到一个 8 字符的 code，您——bot 所有者——运行 `openclaw pairing approve <channel> <CODE>` 来激活他们。Codes 在一小时后过期。

---

## 完整逐步指南：批准 pairing code

### 步骤 1 — 用户向您的 bot 发送 DM

用户向您的 bot 发送消息（例如，在 Telegram、Discord、WhatsApp 等平台上）。由于他们是未知用户，bot 不会处理他们的消息——它会回复一个 8 字符的 pairing code（大写字母，不包含模糊字符如 0、O、1 和 I）。

---

### 步骤 2 — 用户与您分享 code

用户必须告诉您（bot 所有者）他们的 pairing code 是什么——例如：`JN4MSY23`

---

### 步骤 3 — 检查待处理的 pairing 请求（可选）

在您的 Linux 服务器上运行：

```bash
openclaw pairing list telegram
```

将 `telegram` 替换为您的 channel：`telegram`、`whatsapp`、`signal`、`imessage`、`discord`、`slack`

---

### 步骤 4 — 批准 pairing code

```bash
openclaw pairing approve <channel> <CODE>
```

**按平台示例：**

```bash
# Telegram
openclaw pairing approve telegram JN4MSY23

# Discord
openclaw pairing approve discord JN4MSY23

# WhatsApp
openclaw pairing approve whatsapp JN4MSY23

# Slack
openclaw pairing approve slack JN4MSY23

# Signal
openclaw pairing approve signal JN4MSY23

# LINE
openclaw pairing approve line JN4MSY23
```

您应该看到确认消息：`Approved telegram sender <user-id>`

---

### 如果在 Docker 中运行

首先进入容器，然后运行 approve 命令：

```bash
# SSH into your server
ssh root@YOUR_SERVER_IP

# Enter the OpenClaw container
docker exec -it openclaw-mupw-openclaw-1 sh

# Approve the pairing code
openclaw pairing approve telegram ABCD1234

# Exit container
exit

# Restart the container
docker restart openclaw-mupw-openclaw-1
```

---

### 如果使用 Docker Compose 运行

从包含 `docker-compose.yml` 的文件夹直接通过 Docker Compose 运行 approve 命令：

```bash
docker compose run --rm openclaw-cli pairing approve telegram <CODE>
```

---

### 通过 Web UI（Dashboard 聊天框）

在 OpenClaw web 界面聊天框中输入：

```
openclaw pairing approve telegram <CODE>
```

---

## 重要说明

| Topic | Details |
|---|---|
| Code expiry | Codes expire after **1 hour** — if missed, the user must send another message to get a new code |
| Max pending codes | Pending DM pairing requests are capped at 3 per channel by default; additional requests are ignored until one expires or is approved |
| After approval | The user is added to a local allowlist and can now interact with the bot normally |
| Approve all pending | `openclaw pairing approve telegram` (no code = approve all pending) |

---

## 永久授权（生产环境推荐）

通过 pairing code 批准后，切换到 **allowlist 模式**，这样用户无需重新 pairing：

```bash
# Set dmPolicy to allowlist and add user's Telegram numeric ID
openclaw config set channels.telegram.dmPolicy allowlist
openclaw config set channels.telegram.allowFrom '["123456789"]'
openclaw restart
```

Telegram 需要数字 ID，而不是 @usernames。WhatsApp 需要 E.164 格式，如 `+15551234567`。Discord 需要完整的数字用户 ID。

参考资料：

- [OpenClaw Pairing Docs (official)](https://docs.openclaw.ai/channels/pairing)
- [OpenClaw Pairing Explained - Stack Junkie](https://www.stack-junkie.com/blog/openclaw-pairing-explained)
- [Connect Telegram to OpenClaw on VPS - Medium](https://medium.com/@mikhela65/how-to-connect-telegram-to-openclaw-on-hostinger-vps-control-your-ai-agent-from-anywhere-532ab7003d0e)
- [Running OpenClaw in Docker - Simon Willison](https://til.simonwillison.net/llms/openclaw-docker)
- [OpenClaw Pairing Docs - LearnClawdbot](https://www.learnclawdbot.org/docs/start/pairing)
- [OpenClaw GitHub README](https://github.com/openclaw/openclaw/blob/main/README.md)
