---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw中Nextcloud Talk机器人配置
translated: true
type: note
---

**问题：** 如何在 OpenClaw（AI 代理）中设置 Nextcloud Talk，以及为什么无法将机器人添加到房间？

**回答：**

## 在 OpenClaw 中设置 Nextcloud Talk

Nextcloud Talk 在 OpenClaw 中通过一个插件（webhook bot）获得支持。它支持直接消息、房间消息、反应和 Markdown 消息。它**不**随核心安装包捆绑提供——你必须单独安装它。

---

### 步骤 1：安装 Nextcloud Talk 插件

通过 CLI 从 npm 注册表安装：

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

或者，如果从本地的 git 检出目录运行：

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

---

### 步骤 2：在你的 Nextcloud 服务器上注册机器人

SSH 登录你的 Nextcloud 服务器并运行 OCC 命令：

```bash
./occ talk:bot:install "OpenClaw" "<共享密钥>" "<webhook-url>" --feature reaction
```

将 `<共享密钥>` 替换为一个强壮的、40 个字符以上的密钥，并将 `<webhook-url>` 替换为 Gateway 可公开访问的 webhook 端点（例如 `https://gateway.example.com:8788`）。

---

### 步骤 3：在房间中启用机器人

进入 Nextcloud 中的目标房间设置，然后**启用**你刚刚创建的机器人。

这是一个必需的手动步骤，也是机器人无法添加到房间的最常见原因——**你必须在 Nextcloud Talk 的房间设置中为每个房间显式启用机器人**。

---

### 步骤 4：配置 OpenClaw

更新你的 OpenClaw 配置文件，添加以下最小配置：

```json
{
  "channels": {
    "nextcloud-talk": {
      "enabled": true,
      "baseUrl": "https://cloud.example.com",
      "botSecret": "shared-secret",
      "dmPolicy": "pairing"
    }
  }
}
```

然后重启 gateway 以应用更改。

---

### 为什么无法将机器人添加到房间？（常见问题）

**1. 你忘记了在房间设置中启用机器人。**
通过 OCC 安装后，仍然需要在你想让其可用的每个 Talk 房间中手动启用机器人。

**2. Webhook 无法访问。**
你的 Nextcloud 服务器必须能够向 OpenClaw Gateway 发送数据。如果你在反向代理后面，请确保在配置中设置 `webhookPublicUrl`。

**3. 直接消息被当作房间消息处理。**
标准的 webhook 负载无法区分直接消息和房间消息。要解决此问题，请提供 `apiUser` 和 `apiPassword`，以便插件可以执行房间类型查找。

**4. 房间白名单 / groupPolicy 阻止了机器人。**

默认情况下，`groupPolicy` 设置为 `"allowlist"`（提及触发）。你必须像这样显式地将房间加入白名单：

```json
{
  "channels": {
    "nextcloud-talk": {
      "rooms": {
        "room-token": { "requireMention": true }
      }
    }
  }
}
```

若要不允许任何房间，请将 allowlist 留空或设置为 `groupPolicy: "disabled"`。

---

### 直接消息配对流程

默认情况下，OpenClaw 对直接消息使用“配对”模型。当有人第一次向机器人发送消息时，他们会收到一个配对码。然后管理员批准它：

```bash
openclaw pairing list nextcloud-talk
openclaw pairing approve nextcloud-talk <CODE>
```

对于更广泛的部署，你可以切换到开放策略：

```json
"dmPolicy": "open",
"allowFrom": ["*"]
```

---

### 已知限制

- **不支持话题线程** — 机器人的每次回复都发送到主对话。
- **媒体仅限 URL** — 机器人无法直接上传文件；它只发送 URL 链接。
- **机器人无法发起直接消息** — 用户必须先向机器人发送消息以建立连接。

参考资料：

- [OpenClaw Nextcloud Talk 官方文档](https://docs.openclaw.ai/channels/nextcloud-talk)
- [将 OpenClaw AI 代理连接到 Nextcloud Talk – Team 400 博客](https://team400.ai/blog/2026-04-openclaw-nextcloud-talk-ai-agents)
- [OpenClaw Nextcloud Talk 设置指南](https://open-claw.me/channels/nextcloud)
- [OpenClaw GitHub README](https://github.com/openclaw/openclaw/blob/main/README.md)
- [Claw 文档 – Nextcloud Talk](https://docs.claw.so/engine/channels/nextcloud-talk/)
