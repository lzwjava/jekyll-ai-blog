---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 探索 OpenClaw 开源 AI 智能体
translated: true
type: note
---

**Question:** 什么是 OpenClaw (🦞)？该用户的使用体验如何体现了它的核心功能 —— 包括软件安装、作为 Router 使用、运行多个 Instance、升级 Ubuntu、Token 使用情况、模型偏好、与 Nextcloud Chat 的配置以及 LAN/SSH 控制？

**Answer:**

## 什么是 OpenClaw？

OpenClaw（前身为 Clawdbot，后更名为 Moltbot）是一个免费且开源的自主 AI Agent，它通过 Large Language Models (LLMs) 执行任务，并以即时通讯平台作为主要用户界面。它由奥地利开发者 Peter Steinberger 开发，于 2025 年 11 月首次发布。

OpenClaw 的独特之处在于其组合特性：采用 MIT 许可证、开源、Local-first（Memory 和数据以 Markdown 文件形式存储在本地磁盘），并且通过便携式的 Skill 格式支持社区扩展。

“龙虾”昵称 (🦞) 源于其吉祥物 —— 太空龙虾 Molty，因此用户通常亲切地称其为“龙虾”。

---

## 拆解该用户的 OpenClaw 使用体验

### 1. 构建 7 个软件工具（包括本地 NAS 搜索引擎）

OpenClaw 能将 LLMs 连接到真实软件。通过简单的聊天指令，它可以读写文件、运行 Shell 命令、浏览网站、发送电子邮件并控制 API —— 它是真正去执行步骤，而不仅仅是解释如何操作。该用户将其作为 AI Agent 来辅助安装和配置多个 Self-hosted 应用（例如局域网网盘/NAS 搜索引擎），本质上是利用 AI 以交互方式处理繁琐的安装步骤。

### 2. 尝试将 Linux 主机用作 Router（失败 —— 太复杂）

这是一个常见的高级用例。OpenClaw 可以在 Linux 机器上运行 Shell 命令，因此用户尝试让它配置 Routing/NAT/iptables。用户发现这太复杂了 —— 这是一个客观的评价；将普通的 Linux 盒子变成功能完善的 Router 涉及许多底层的 Networking 配置，即使是 AI Agent 也难以可靠地实现端到端的自动化。

### 3. 运行两个 OpenClaw Instances

OpenClaw 通过其 Multi-agent 路由系统，支持按 Agent、Workspace 或发送者隔离 Session。用户部署了两个独立的 OpenClaw “龙虾” —— 可能是一台机器一个，或者按用例区分 —— 这是一个受支持且常见的配置。

### 4. 使用 OpenClaw 升级 Ubuntu 22 → 24

这是一个实用的 Power-user 操作。由于 OpenClaw 可以执行宿主机的 Shell 命令，用户指示 AI 运行 `do-release-upgrade` 进程并处理过程中的交互式提示。AI 充当了引导和执行升级步骤的助手。

### 5. Token 使用情况：每周约 70M Claude tokens + 每周约 50M OpenRouter tokens

AI 模型可以是云端托管的（Anthropic, OpenAI, Google），也可以是本地的（通过 Ollama, LM Studio 或其他兼容 OpenAI 的 Server），具体取决于配置。该用户是一个重度使用者 —— 直接通过 Anthropic 使用 Claude 作为主要 Backend，并同时通过 OpenRouter（一个提供多种模型访问权限的 API 聚合器）调度流量。约 120M tokens/周的总量表明这是一个高度自动化、常驻运行的 Agentic 系统。

### 6. 小米 V2 模型表现良好

小米发布了 AI 模型（MiMo 系列）。用户通过 OpenRouter 对其进行了测试，发现表现不错。OpenClaw 的 Model-agnostic 设计使其可以轻松地在不同 Provider 之间切换并测试不同的 LLMs，而无需重新配置整个 Agent。

### 7. 配置 Nextcloud Talk (Chat)

OpenClaw 支持将 Nextcloud Talk 作为其消息通道集成之一。用户将 OpenClaw 接入了 Nextcloud Talk（Nextcloud 的自托管聊天组件），并使用 Claude 作为底层模型。这意味着他们可以直接在自托管的 Nextcloud 环境中与 AI Agent 聊天。

### 8. Memory 与 Plugins —— 尚未尝试

OpenClaw 将对话及 Long-term memory 以纯 Markdown 和 YAML 文件形式存储在 Workspace 和 `~/.openclaw` 目录下。Memory 系统和 Skill/Plugin 生态系统是该用户计划下一步探索的高级功能。用户可以使用超过 100 个预配置的 AgentSkills 来扩展工具的能力，这些 Skill 允许 AI 执行 Shell 命令、管理文件系统并进行 Web 自动化。

### 9. 通过 SSH 控制其他 LAN 机器

这是 OpenClaw 最强大的实际用途之一。OpenClaw 专为开发者和 Power users 设计，他们希望拥有一个可以随时发消息、且无需牺牲数据控制权或依赖第三方托管服务的个人 AI 助手。只要局域网内的各主机之间配置了 SSH，用户就可以向 OpenClaw 发送聊天消息，让它 SSH 登录到另一台机器并运行命令 —— 从而将 OpenClaw 变成一个贯穿整个本地网络的自然语言远程管理工具。

---

## 总结表

| 体验项目 | 使用的 OpenClaw 功能 |
|---|---|
| 7 个软件安装 | Shell commands + Skill automation |
| Router 尝试 | Shell/Networking 命令（复杂，失败）|
| 两个 Instances | Multi-agent / Multi-workspace 支持 |
| Ubuntu 升级 | 在宿主机上执行 Shell 命令 |
| 每周 70M + 50M tokens | 多 Provider 模型 Backend 支持 |
| 小米 V2 模型 | Model-agnostic，支持通过 OpenRouter 使用 |
| Nextcloud Talk 集成 | 原生 Nextcloud Talk Channel 支持 |
| Memory/Plugins | 尚未探索（计划中） |
| SSH LAN 控制 | Shell + 对远程主机的 SSH 访问 |

**参考资料：**

- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [OpenClaw Official Site](https://openclaw.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Milvus Blog — OpenClaw Complete Guide](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [DigitalOcean — What is OpenClaw](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [KDnuggets — OpenClaw Explained](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)