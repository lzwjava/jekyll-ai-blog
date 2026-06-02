---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Moltbot 您的私人本地人工智能助手
translated: true
type: note
---

我非常乐意为您全面介绍 clawdbot，但我需要先搜索关于它的最新信息，因为这似乎是一个特定的工具或产品，我应该获取其最新的详细信息。

# Comprehensive Introduction to Clawdbot (现更名为 Moltbot)

**Clawdbot** 最近已更名为 **Moltbot** —— 这是一个在您自己的电脑上运行而非云端运行的开源个人 AI assistant。您可以将其视为一个由您完全控制、通过您已在使用的 messaging apps 即可访问的私有 AI。

## What Is It?

Moltbot 是一个运行在本地机器上的个人 AI assistant，它可以连接到您已在使用的 messaging platforms，如 WhatsApp、Telegram、Discord、Slack 等。与基于云的 AI services 不同，您的数据保留在自己的设备上，且您可以完全控制其运行方式。

## Key Features

**Multi-Channel Access**：您可以通过 WhatsApp、Telegram、Discord、Slack、Signal、iMessage、Microsoft Teams、Matrix、Zalo 和 WebChat 与 Moltbot 交互。它支持 direct messages 和 group chats。

**Persistent Memory**：该 assistant 会跨 sessions 记住您的对话和偏好，随着时间的推移建立起对您需求的个性化理解。

**System Access**：Moltbot 可以读写 files、运行 shell commands、执行 scripts，并拥有完整的 system access —— 尽管为了安全起见，您可以选择将其置于 sandbox 中运行。

**Browser Control**：它可以自动浏览 web、填写表格并从网站提取数据。

**Skills & Plugins**：您可以通过社区创建的 skills 扩展功能，或构建自己的技能。该 assistant 甚至可以编写自己的 skills。

**Voice Capabilities**：在 macOS、iOS 和 Android 上，它支持 voice wake commands 以及用于免提交互的 talk mode。

## How It Works

Moltbot 在您的电脑上运行一个 Gateway control plane，该平面将 messaging channels 连接到由 Claude 或 GPT 等 models 驱动的 AI agent。Gateway 在以下各项之间进行协调：

- 您的 messaging apps (WhatsApp, Telegram 等)
- AI model (Claude, GPT, 或 local models)
- System tools (browser, files, commands)
- 可选的 companion apps (macOS menu bar, iOS/Android)

## Installation

最简单的 installation 方法需要 Node.js 22 或更高版本，并使用一个简单的 npm 命令：`npm install -g clawdbot@latest`，随后运行 `clawdbot onboard --install-daemon`，它将引导您完成 setup。

## Security Considerations

这一点非常重要：默认情况下，当您直接使用 Moltbot (main session) 时，它拥有完整的 system access。然而，对于 group chats 或 channels，您可以将其配置为在具有受限权限的 sandboxed Docker containers 中运行。

对于 messaging channels，Moltbot 对未知联系人使用 pairing system —— 他们会收到一个 code，您必须在 bot 处理他们的消息之前批准他们。

## Recent Developments

**Important Security Alert**：近期有报告称，出现了冒充 Clawdbot/Moltbot 的虚假 VS Code extensions 并安装 malware。请务必仅从官方渠道（GitHub repository 或 npm）安装。

该项目引起了巨大的轰动，在 GitHub 上获得了超过 51,000 个 stars，并得到了社区的积极反馈。许多用户将其描述为感觉像是“活在未来”，并将其比作终于拥有了一个真正的 Jarvis 式 assistant。

## Who Created It?

Moltbot 由 Peter Steinberger 和开源社区为 "Clawd"（被描述为一个太空龙虾 AI assistant）构建。这是一个采用 MIT license 的独立项目，欢迎社区贡献。

## Use Cases

人们正在将 Moltbot 用于：

- Email management 以及退订垃圾邮件
- Calendar management 和行程提醒
- 自动化 coding tasks 和 workflows
- Document processing 和研究
- Home automation 集成
- 创建自定义 workflows 和 automations

该项目代表了向真正 personal AI 的转变 —— 运行在您的 infrastructure 上，学习您的偏好，在保持数据私密性的同时与您的数字生活深度集成。
