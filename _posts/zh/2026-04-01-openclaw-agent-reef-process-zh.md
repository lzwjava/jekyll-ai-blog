---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 代理礁流程说明
translated: true
type: note
---

我会搜索关于 openclaw AI agent 中 kind-reef 的信息来解释过程。让我更具体地搜索“reef”作为 OpenClaw agent 的名称。根据我的搜索结果，我现在有足够的信息来解释涉及“kind-reef”的过程（这似乎是一个命名示例，其中“Reef”是特定 OpenClaw agent 的名称）。让我提供全面解释。

---

**问题：** 你能解释 OpenClaw（AI agent）中“kind-reef”的过程吗？

**回答：**

根据搜索结果，“kind-reef”似乎指的是 OpenClaw 中的命名约定，其中“Reef”是特定 AI agent 实例的名称。开发者 Nathan 创建了一个名为“Reef”的 AI agent，运行在他的家庭服务器上。让我解释一般的 OpenClaw agent 过程以及像“Reef”这样的自定义命名 agent 的工作方式：

## What is OpenClaw?

OpenClaw 是一个免费开源的自主人工智能 agent，它通过大型语言模型（LLMs）执行任务，使用消息平台作为主要用户界面。与典型的聊天机器人不同，这个工具实际上可以在你的计算机上执行任务，用户利用它来自动化工作流、管理文件、发送电子邮件以及控制 APIs。

## The Agent Architecture

当你运行 openclaw gateway 时，你会启动一个单一的长寿 Node.js 进程称为 Gateway，这是整个系统——通道连接、会话状态、agent 循环、模型调用、工具执行和内存持久化。工作流程如下：

1. **消息接收**：你在消息界面（WhatsApp、Telegram、Slack、Discord 等）中输入命令
2. **解释**：LLM 模型解释指令并决定必要的行动
3. **执行**：OpenClaw 使用其“skills”执行任务，例如 shell 命令、浏览器或 APIs
4. **完成**：结果发送回 agent，直到任务完成

## Agent Naming and Identity

OpenClaw 使用 skills 系统，其中 skills 存储为包含 SKILL.md 文件的目录，该文件带有元数据和工具使用说明。每个 agent 可以有自定义身份：

- **Agent Name**：用户为他们的 agent 选择自定义名称（如“Reef”、“Jarvis”、“Polly”等）
- **Identity Configuration**：用户可以使用命令如 `openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png` 设置身份
- **Personality**：agent 的行为和个性通过配置文件定义

## The "Reef" Example

Reef 是一个运行在家庭服务器上的 OpenClaw agent，通过 SSH 访问整个家庭服务器基础设施，包括家庭网络中的所有服务器和容器。这个特定实现展示了高级功能：

**Automated Tasks**：Reef 运行 15 个自动化任务，包括 Active Work Session 检查、用于监控健康检查的 Alerts Check、用于扫描收件箱的 Gmail Triage，以及用于处理笔记的 KB Data Entry Batch。

**Self-Sustaining Operations**：Reef 执行 Self Health Checks，包括运行 openclaw doctor、检查内存/磁盘、审查日志，以及每天早上 8 点的 Daily Briefing，发送包含天气、日历和系统统计的电子邮件摘要。

**Application Development**：Reef 从零构建并部署了一个完整的 web app，名为 Neat，使用 SvelteKit、TypeScript、Tailwind、SQLite，并部署到 Kubernetes，使用 Woodpecker CI。

## Multi-Agent Capabilities

用户可以通过 `openclaw agents add agent_name` 运行多个 agent，这会让他们再次进行 onboarding，创建一个全新的 agent，具有完全独立的身份、工具集、crons 和 workspace。

## Storage and Memory

OpenClaw 将对话、长期内存和 skills 存储为位于你的 workspace 和 ~/.openclaw 下的纯 Markdown 和 YAML 文件，你可以用任何文本编辑器检查它们，用 Git 备份它们，grep 搜索它们，或删除它们。

## Security Considerations

OpenClaw 的设计引起了网络安全研究人员的关注，因为该软件可以访问电子邮件账户、日历、消息平台和其他敏感服务，配置错误或暴露的实例会带来安全和隐私风险。该 agent 还容易受到 prompt injection attacks，即在数据中嵌入有害指令，意图让 LLM 将其解释为合法用户指令。

## Summary

OpenClaw 中的“kind-reef”概念代表了创建个性化、命名 AI agent 的能力，这些 agent 具有特定的身份和功能。“Reef”作为一个真实世界的示例，展示了用户如何使用独特的名称、个性和任务自动化配置来自定义他们的 OpenClaw 实例。该 agent 持续运行，执行计划任务、监控系统，并通过消息平台响应用户请求，同时在会话间保持持久内存和上下文。

**参考文献：**

- [https://en.wikipedia.org/wiki/OpenClaw](https://en.wikipedia.org/wiki/OpenClaw)
- [https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)
- [https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [https://docs.openclaw.ai/cli/agents](https://docs.openclaw.ai/cli/agents)
- [https://madebynathan.com/2026/02/03/everything-ive-done-with-openclaw-so-far/](https://madebynathan.com/2026/02/03/everything-ive-done-with-openclaw-so-far/)
- [https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building)