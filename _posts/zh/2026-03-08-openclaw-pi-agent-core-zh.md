---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 架构与 Pi 代理核心
translated: true
type: note
---

**问题：** OpenClaw 是如何工作的？它使用 Pi agent library 吗？它的核心机制是什么？

**回答：**

## 什么是 OpenClaw？

OpenClaw（前身为 Clawdbot 和 Moltbot）是由 Peter Steinberger 开发的一个免费开源的自主 AI 代理。它是一个自主代理，可以通过大型语言模型执行任务，使用消息平台作为其主要用户界面。其功能通过消息服务（如 Signal、Telegram、Discord 或 WhatsApp）中的聊天机器人访问。配置数据和交互历史本地存储，从而实现跨会话的持久性和自适应行为。

---

## 是的——OpenClaw 使用 Pi Agent Library

OpenClaw 使用 Pi SDK 将 AI 编码代理嵌入其消息网关架构中。OpenClaw 不是将 Pi 作为子进程启动或使用 RPC 模式，而是直接导入并实例化 Pi 的 `AgentSession`，通过 `createAgentSession()`。

Pi library 是一个由 Mario Zechner（libGDX 的创建者）创建的 TypeScript monorepo。它由四个分层包组成：

- `pi-ai` — 处理跨提供商的 LLM 通信（流式传输、多提供商）
- `pi-agent-core` — 添加代理循环，包括工具调用和事件发射
- `pi-coding-agent` — 完整的编码代理，内置工具、会话持久性和可扩展性
- `pi-tui` — 用于构建 CLI 接口的终端 UI

SDK 处理完整的代理循环：发送至 LLM、执行工具调用，并流式传输响应。

---

## 核心架构：六个层

### 1. Gateway（前门）
OpenClaw 以单个 Node.js 进程在您的机器上运行，默认监听 `127.0.0.1:18789`。这个进程称为 Gateway，它同时管理每个消息平台连接——WhatsApp、Telegram、Discord、Slack、Signal 等。来自任何平台的每条消息都通过 Gateway 传入。代理生成的每个响应都通过它返回。

### 2. Channel Adapters（输入规范化）
OpenClaw 支持十多个通道。通道集成将所有输入规范化成单个一致的消息对象，包括发件人、正文、任何附件和通道元数据。如果您发送语音笔记，它会在到达模型之前被转录为文本。

### 3. Pi Agent Loop（核心引擎）
`pi-agent-core` 中的核心代理循环有意保持最小化。它：
1. 流式传输 LLM 响应
2. 如果没有工具调用，则结束
3. 顺序执行工具
4. 将工具结果添加回上下文并继续

OpenClaw 拥有整个执行环境，仅将 Pi 用作代理循环引擎。OpenClaw 订阅 Pi 的事件流，该流经过：`agent_start → turn_start → message_start → text_delta → tool_execution_start → tool_execution_update → tool_execution_end → message_end → turn_end → agent_end`。每个事件都被路由到适当的处理程序：文本增量变为流式聊天回复，工具执行被记录为 JSONL 转录。

### 4. Tool System
OpenClaw 的工具集是分层的：
- **Base tools**：Pi 的内置编码工具（read、bash、edit、write）
- **Custom replacements**：OpenClaw 用 `exec/process` 替换 `bash`，并为沙箱自定义文件工具
- **OpenClaw-specific tools**：messaging、browser、canvas、sessions、cron、gateway 等
- **Channel tools**：Discord/Telegram/Slack/WhatsApp 特定的操作工具
- **Policy filtering**：工具按 profile、provider、agent、group 和 sandbox 策略过滤

### 5. Memory System（基于文件）
OpenClaw 通过简单的文本文件维护内存。有一个 `agents.md` 文件存储代理配置的一切，以及一个 `soul.md` 文件，其中代理的个性随时间构建。

对于内存检索，OpenClaw 支持基于 embedding 的搜索，可选由 `sqlite-vec` SQLite 扩展加速。没有外部数据库、没有 Redis、没有 Pinecone——只需 SQLite 和 Markdown 文件。

### 6. Lane Queue System（并发控制）
OpenClaw 引入“lane queue”系统。每个会话都有自己的 lane。该 lane 中的任务默认串行执行。对于大型项目，并行文件写入可能导致合并冲突；串行执行提高了可重现性并减少了意外混乱。

### 7. Context Compaction
OpenClaw 通过压缩管道管理上下文溢出：Context Window Guard 持续监控令牌计数，软阈值首先触发以静默刷新内存，然后压缩将较旧的轮次总结为紧凑表示。在 JSONL 树中创建一个新分支，以摘要作为根。

### 8. Heartbeat（主动代理）
OpenClaw 更有趣的地方之一是它不仅仅坐等您发消息。它运行一个 heartbeat——默认每 30 分钟触发一次的定时触发器。每次 heartbeat 时，代理读取 `HEARTBEAT.md`，这是一个它应主动检查的任务清单。如果某事需要关注，它会采取行动并可能给您发消息。

### 9. Skill System
OpenClaw 使用基于技能的架构，其中能力定义在 Markdown 文件中，而不是编译代码。每个技能位于 `~/clawd/skills/<skill-name>/SKILL.md`，包含与 API 交互或执行工作流的说明。代理在运行时读取这些文件以了解可用能力。安装立即生效——无需重新编译或服务器重启。

---

## 总结

OpenClaw 本质上是一个基于 Pi SDK 的**多通道 AI 代理运行时**。Pi 提供原始代理循环（LLM → 工具调用 → 循环），而 OpenClaw 在其上添加了生产级层：消息网关、持久文件内存、基于 lane 的并发、上下文压缩、主动 heartbeat 调度，以及模块化的 Markdown 技能系统。

**参考资料：**

- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [Pi Integration Architecture — OpenClaw Docs](https://docs.openclaw.ai/pi)
- [Pi Integration Architecture — claw.so Docs](https://docs.claw.so/engine/pi/)
- [Anatomy of a minimal coding agent powering OpenClaw — Medium](https://medium.com/@shivam.agarwal.in/agentic-ai-pi-anatomy-of-a-minimal-coding-agent-powering-openclaw-5ecd4dd6b440)
- [Inside OpenClaw: How it Actually Works — DEV Community](https://dev.to/jiade/inside-openclaw-how-the-worlds-fastest-growing-ai-agent-actually-works-under-the-hood-4p5n)
- [How OpenClaw Works — Medium](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)
- [How to Build a Custom Agent Framework with Pi — Nader's Substack](https://nader.substack.com/p/how-to-build-a-custom-agent-framework)
- [Inside OpenClaw: Persistent AI Agent — DEV Community](https://dev.to/entelligenceai/inside-openclaw-how-a-persistent-ai-agent-actually-works-1mnk)
- [OpenClaw Architecture Guide — Vertu](https://vertu.com/ai-tools/openclaw-clawdbot-architecture-engineering-reliable-and-controllable-ai-agents/)
- [OpenClaw AI Agent Masterclass — HelloPM](https://hellopm.co/openclaw-ai-agent-masterclass/)