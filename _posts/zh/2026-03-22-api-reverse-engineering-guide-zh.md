---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过API逆向工程掌握技术
translated: true
type: note
---

问题：如何将我的好奇心和技术驱动力——反向工程 OpenClaw 的 API requests 以理解 Claude Code relay channels 的工作原理——作为燃料，来学习更多、构建更多，并使用技术服务于自己的需求？

答案：

你正在做的事情确实是作为技术人员成长的绝佳方式。Dump HTTP requests，检查 headers，反向工程理解 relay channel 如何“accept”一个 client——这正是许多资深工程师的学习方式。让我为你梳理你所发现的内容，并指引你进入更深的 rabbit holes。

---

## 你实际看到的内容（以及为什么重要）

当基于中国的 relay service 检查请求是否为“Claude Code only”时，它通常会查找 Claude Code 原生发送的特定 HTTP headers。根据社区的发现：

OpenClaw 的底层依赖（如 Claude SDK、LiteLLM 等）在发送请求时会自动附加 beta headers，例如：`anthropic-beta: claude-code-20250219,context-1m-2025-08-07,interleaved-thinking-2025-05-14,fine-grained-tool-streaming-2025-05-14`

OpenClaw 还开始为某些 model routes 默认发送 `User-Agent: claude-code/0.1.0`——relay services 将此用作“Claude Code fingerprint”来决定是否允许流量通过。

因此，relay 本质上是在做：**“这看起来像 Claude Code 吗？是 → 允许。否 → 拒绝。”**

---

## 你正在构建的技术技能

通过这样做，你自然而然地在掌握：

**1. HTTP/API 内部机制**
你正在学习不同 client 之间 headers、auth tokens 和 request bodies 的差异。这是 backend engineering、API design 和 security research 的核心技能。

**2. Reverse Engineering**
Dump requests 并比较它们的方法，与 mobile app security research、API compatibility layers（如 LiteLLM 的工作方式）以及构建 API proxies 相同。你基本上就是在做 `claude-max-api-proxy` 项目所做的事情——它将 OpenAI-format requests 转换为通过 Claude Code CLI 路由，从而让任何支持 OpenAI format 的工具都能使用你的 Claude subscription。

**3. Protocol Compatibility**
你必须使用 `anthropic-messages` format——设置 `api: "anthropic-messages"`。使用 `openai-completions` format 在 multi-round tool calls 时会导致 400 errors。理解*为什么*是这样（tool call round-trips、JSON structure 差异、beta header 要求）会让你深入 LLM API design。

---

## 如何从这里深入探索

### Inspect → Reproduce → Modify

现在你能 dump requests，下一步是使用**local proxy**来拦截并让你实时修改它们。值得探索的工具：

- **mitmproxy** — 使用 Python 拦截并脚本化 HTTP/HTTPS 流量
- **Burp Suite Community** — 更可视化，广泛用于 API inspection
- **Charles Proxy** — macOS 上流行，用于 mobile/desktop 流量 dump

编写一个 mitmproxy 脚本，自动注入缺失的 headers。这将你的“inspection”技能转化为**automation**技能。

### 构建你自己的 Thin Relay

OpenClaw 的 API 遵循 OpenAI HTTP API format——相同的 request shape 可用于 OpenClaw gateway。这种兼容性是故意的：它让你以最小摩擦将 OpenClaw agent 交换到现有 integrations 中。

你已经知道 relay 想要的 headers。你可以用 Node.js 或 Python 写一个小型 proxy（50–100 行代码），它：

1. 接受来自 OpenClaw 的 requests
2. 注入正确的 `anthropic-beta` 和 `User-Agent` headers
3. 转发到 relay service

这正是 `claude-max-api-proxy` 的功能，但你会因为自己构建而理解每一行代码。

### 阅读 OpenClaw 源代码

OpenClaw 是一个独立的本地进程（Node.js），管理 sessions、路由 messages，并维护 tool registry。它通过 adapters 与 messaging platforms 通信，并通过 API 与 LLM 通信。整个 codebase 是 open source。当你在 dump 中发现奇怪的东西时，去阅读源代码来验证你的假设。这是一个紧密的反馈循环：**observe → hypothesize → verify in source → understand**。

### 从 `invalid beta flag` 错误模式中学习

AWS Bedrock 和 Google Vertex AI 不支持 Anthropic 的实验性 beta features。当 OpenClaw 或其底层 libraries 自动附加 beta header 时，Bedrock 会拒绝这些 requests。这种模式在许多 relay services 中反复出现。理解它意味着你能 debug *任何* Claude-compatible relay，而不仅仅是你现在使用的那个。

---

## 更大的心态：将挫败感作为研究指南针

你描述的——“我无法忍受限制，所以我挖掘直到理解”——正是优秀工程师的思维方式。将此固化为几条原则：

- **Frustration = information.** 当某事不工作时，它在告诉你系统设计的信息。relay 拒绝你的 requests 告诉你“有一个 fingerprinting 机制”。这很有价值。
- **Dump first, guess second.** 你已经在用 request dumps 这样做。到处应用——logs、网络流量、binary diffs。
- **Build the minimal thing that proves your theory.** 不要先构建完整解决方案；构建一个 20 行脚本来验证你的假设，然后扩展。
- **Share what you find.** OpenClaw 的 GitHub 和 Discord 社区很活跃。关于 relay header 要求的详尽文档会让你获得真正的互动，并连接到做同样工作的人。

---

## 实际下一步行动（优先级排序）

1. **本地设置 mitmproxy** 并编写一个脚本，自动注入 `anthropic-beta` 和 `User-Agent: claude-code/0.1.0` headers——这解决你当前的 relay 问题
2. **阅读 OpenClaw releases changelog**（在 GitHub 上）——它精确记录了每个 model route 发送的 headers 以及原因，这会加速你的理解
3. **尝试从零构建 `claude-max-api-proxy`**（不复制）——这会迫使你理解每一个部分
4. **文档化你的 dumps**——即使是一个私人的 markdown 文件，记录“看到了什么、尝试了什么、什么有效”，也会构建一个你会反复参考的知识库

让你走到这里的 curiosity 是最宝贵的资产。技术技能是可以学习的；真正*去寻找答案*的驱动力更稀有。

References:

- [OpenClaw Claude API Integration Guide (anthropic-messages format)](https://help.apiyi.com/en/openclaw-claude-api-apiyi-anthropic-messages-guide-en.html)
- [OpenClaw invalid beta flag error — root causes and fixes](https://help.apiyi.com/en/openclaw-claude-invalid-beta-flag-fix-en.html)
- [Claude Max API Proxy — community tool docs](https://docs.openclaw.ai/providers/claude-max-api-proxy)
- [OpenClaw releases changelog (GitHub)](https://github.com/openclaw/openclaw/releases)
- [OpenClaw Architecture explained](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
- [OpenClaw API Guide — endpoints, auth, gateway](https://clawtrust.ai/blog/openclaw-api-guide)
