---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw WhatsApp设置指南
translated: true
type: note
---

**老大，以下是针对你设置的WhatsApp解决方案：**

## OpenClaw中的WhatsApp

OpenClaw使用 **WhatsApp Web (Baileys)** —— 通过扫描服务器生成的二维码来链接你的WhatsApp账户。这适用于iOS版的普通WhatsApp和WhatsApp Business。

### 步骤：

**1. 安装WhatsApp插件**（如果尚未安装）：
```bash
openclaw plugins install @openclaw/whatsapp
```

**2. 在 `openclaw.json` 中配置访问策略**：
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",       // 或者如果你预先添加了号码，可使用 "allowlist"
      allowFrom: ["+852XXXXXXXX"], // 你的手机号（E.164格式）
    },
  },
}
```

**3. 通过二维码链接**：
```bash
openclaw channels login --channel whatsapp
```
这将在你的终端显示一个二维码。在你的iPhone上：
- 打开 **WhatsApp**（或WhatsApp Business）
- 进入 **设置 → 关联设备 → 关联一个设备**
- 扫描二维码

**4. 启动网关**：
```bash
openclaw gateway
```

**5. 第一条消息 = 配对**（如果使用 `pairing` 策略）：
从你的手机给你链接的WhatsApp号码发送一条消息，它会给你一个代码，然后：
```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <代码>
```

### 几点说明：

- **建议使用专用号码** —— 为OpenClaw使用单独的WhatsApp号码可避免自我聊天的混淆。但个人号码也可用。
- **WhatsApp Business没问题** —— 链接过程相同，没有区别。
- 鉴于你一直遇到配对码过期问题，可考虑使用 `dmPolicy: "allowlist"` 并预先填入你的号码 —— 完全跳过配对流程。
- 链接后，会话会持续保存（Baileys将凭据存储在 `~/.openclaw/credentials/whatsapp/` 中）。除非你解除链接，否则无需重新扫描。

需要我帮你设置吗？我可以编辑配置并启动登录流程。 🦞
