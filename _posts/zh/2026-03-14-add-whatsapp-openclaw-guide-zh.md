---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 WhatsApp 添加到 OpenClaw 指南
translated: true
type: note
---

## 在 OpenClaw 中添加 WhatsApp 作为通道

OpenClaw 支持从单个 Gateway 实例运行多个通道（WhatsApp、Telegram、Discord、Slack 等）。以下是添加 WhatsApp 的完整指南。

---

### 工作原理

OpenClaw 使用 Baileys 协议（基于 WhatsApp Web）连接到 WhatsApp。它使用“Linked Devices”流程——与 WhatsApp Web 使用的相同功能。您扫描 QR 码，WhatsApp 将您的 OpenClaw 实例链接为伴侣设备。不需要官方 WhatsApp Business API。

---

### 方法 1：通过 `openclaw onboard` 快速设置（推荐用于新设置）

在终端中运行以下命令：

```bash
openclaw onboard
```

运行此命令后，使用箭头键导航交互式菜单：
1. 当提示 **Select channel** 时，选择 **WhatsApp (QR link)** 并按 Enter。
2. 当询问确认时，选择 **Yes**。
3. 使用您的 WhatsApp 手机 **扫描 QR 码**——转到 WhatsApp → Settings → Linked Devices → Link a Device。
4. 如果 QR 码变形，请尝试增加屏幕亮度或调整页面/缩放大小。

---

### 方法 2：向现有 OpenClaw 设置添加 WhatsApp（通过 Config）

**步骤 1 — 编辑您的配置文件**

打开您的配置文件并添加 WhatsApp 通道块：

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": ["+15551234567"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["+15551234567"]
    }
  }
}
```

配置文件通常位于 `~/.openclaw/openclaw.json`。

**步骤 2 — 登录 / 链接您的 WhatsApp 账户**

运行登录命令：

```bash
openclaw channels login
```

会出现 QR 码。使用手机上的 WhatsApp 通过 **Settings → Linked Devices → Link a Device** 扫描它。凭据将保存到 `~/.openclaw/credentials/whatsapp/`。

**步骤 3 — 启动 Gateway**

```bash
openclaw start
```

Gateway 运行后，查看日志中的“WhatsApp connected”以确认链接活跃。

---

### 访问 / DM 策略选项

`dmPolicy` 字段控制谁可以向您的助手发送消息：

- **`pairing`**（默认）——用户必须通过配对请求获得批准。配对请求 1 小时后过期，每个通道的待处理请求上限为 3 个。
- **`allowlist`** —— 仅 `allowFrom` 中列出的号码可以发送消息。
- **`open`** —— 任何人都可以发送消息（需要 `allowFrom` 包含 `"*"`）。
- **`disabled`** —— 不允许 DM。

---

### 同时运行多个通道

您运行一个 OpenClaw Gateway 实例并配置多个通道。来自每个通道的消息将被路由到会话，回复将通过原始通道返回。这意味着您可以使用手机上的 WhatsApp、笔记本上的 Telegram、团队的 Discord 和工作中的 Slack 与同一个助手对话——相同的脑力、相同的记忆、相同的代理。

---

### 故障排除

| 问题 | 解决方案 |
|---|---|
| QR 码已过期 | 重新运行 `openclaw channels login` 并立即扫描 |
| Bot 无响应 | 运行 `openclaw channels status` 检查链接状态 |
| 连接断开 | 在 WhatsApp → Linked Devices 中移除未使用的链接设备，然后重新登录 |
| 重启后未链接 | 删除 `~/.openclaw/credentials/whatsapp/` 并再次运行 `openclaw channels login whatsapp` |
| 一般问题 | 运行 `openclaw doctor` 诊断环境/运行时问题 |

---

### 安全注意事项

由于 WhatsApp 集成依赖第三方包，请验证您安装的是**官方 Baileys 包**，而不是仿冒品。2025 年底，一个名为“lotusbail”的恶意 npm 包冒充 WhatsApp Web API 库并窃取凭据。还推荐使用专用的电话号码，将您的个人聊天与 Bot 分开。

参考资料：

- [OpenClaw WhatsApp Official Docs](https://docs.openclaw.ai/channels/whatsapp)
- [Step-by-step QR Code Connection Guide – LumaDock](https://lumadock.com/tutorials/connect-openclaw-to-whatsapp-qr-code)
- [Multi-channel Setup Guide – LumaDock](https://lumadock.com/tutorials/openclaw-multi-channel-setup)
- [Getting Started with OpenClaw and WhatsApp – MarkTechPost](https://www.marktechpost.com/2026/02/14/getting-started-with-openclaw-and-connecting-it-with-whatsapp/)
- [OpenClaw Add WhatsApp – GoPenAI Blog](https://blog.gopenai.com/openclaw-add-whatsapp-27d9237d3872)
- [DataCamp OpenClaw Tutorial](https://www.datacamp.com/tutorial/moltbot-clawdbot-tutorial)