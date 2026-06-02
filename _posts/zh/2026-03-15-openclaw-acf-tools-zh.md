---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 自主编码框架工具
translated: true
type: note
---

**问题：** OpenClaw 如何处理编程？它使用什么工具？它使用默认模型设置，还是使用 Claude Code 或其他模型进行编程项目？

**回答：**

OpenClaw 是一个开源的、自托管的 AI 代理框架（最初称为 Clawdbot/Moltbot），它在您的机器或 VPS 上本地运行。它充当 AI 代理的编排层或“runtime”，通过消息应用程序（例如 WhatsApp、Telegram、Discord）将大型语言模型 (LLMs) 连接到现实世界的工具和动作。它本身不是 LLM，而是为代理执行任务提供基础设施，包括 **与编程相关的工作**。

### OpenClaw 如何处理编程

- OpenClaw 通过其 **tool-use system** 和 **skills** 实现编程。底层的 LLM（“大脑”）决定何时编写、编辑或执行代码。
- 它可以生成代码、创建脚本、修改文件、运行 shell 命令、管理 git 仓库、自动化浏览器任务，甚至自主编写新的“skills”（自定义工具组合）来改进自身或处理项目。
- 对于软件开发或项目编程，它使用文件读写、shell 执行（`exec`）、浏览器控制以及网络搜索/获取等工具来研究、迭代、测试和部署代码。
- 它在代理循环中运行：观察任务 → 调用工具 → 执行动作 → 反思 → 重复直到完成。这使其适合自主或半自主编程工作流，常被描述为将 LLM 转变为“AI 员工”，能够在您的系统上编程和执行操作。
- 许多用户将其直接与 **Claude Code**（Anthropic 的编程专注 CLI/代理）进行比较，但 OpenClaw 更通用、模型无关，并专注于具有长期记忆和定时“heartbeats”的持久、主动代理。

### 它使用什么工具？

OpenClaw 提供广泛的内置和可扩展 **tools**（有时称为“organs”）和 **skills**（预定义的工作流，结合工具）：

- 核心工具：文件读写、shell 命令执行（`exec`）、网络搜索、页面获取、浏览器自动化（点击、填写表单、截图）。
- 高级工具：内存管理、日历/邮件集成、多会话处理、定时任务（类似 cron 的 heartbeats）。
- 超过 100 个社区构建的 skills 扩展了这些功能，用于 git 操作、代码生成/测试、自动化脚本等任务。
- 编程特定功能来自这些工具的组合：例如，读取项目文件 → 通过 LLM 生成代码 → 写入磁盘 → 执行测试 → 迭代。

### 模型使用（默认设置、Claude 等）

- OpenClaw 是 **model-agnostic** 的——它 **没有** 单一的内置或默认 LLM。您必须连接自己的 API 密钥来自提供商。
- 它支持许多提供商，包括 Anthropic（Claude 模型）、OpenAI（GPT 模型）和其他（例如，通过兼容 API 的本地/开源如 Kimi、Llama、DeepSeek）。
- **配置**：您在配置文件中设置主要模型和备用模型（例如，`agents.defaults.model.primary: "anthropic/claude-opus-4-6"` 或 `"openai/gpt-4o"`）。它按优先级选择：主要 → 备用 → 允许列表模型。
- 许多用户选择强大的编程模型，如 **Claude Opus/Sonnet**（因优秀的推理/tool-use 而非常受欢迎，用于编程）或 GPT 变体。它可以代理通过服务或使用 OpenAI/Anthropic 的编程优化端点。
- 它 **不** 直接“使用 Claude Code”（Anthropic 的独立 CLI 产品）——OpenClaw 是一个独立的 runtime。然而，有些人构建混合体，或将 OpenClaw 设置与 Claude Code 进行比较/替换，用于纯编程任务，因为 Claude Code 在软件工程方面更精炼，但通用自动化灵活性较低。
- 开箱即用 **没有** 固定的“默认模型设置”——设置需要选择并配置一个（通常选择 Claude 系列以获得编程优势）。

简而言之，OpenClaw 通过为强大的 LLM（您选择）提供安全、配备工具的访问您的计算机/文件/系统，从而擅长代理式编程，使其非常适合自主项目——但实际的编程智能来自连接的模型（通常 Claude 变体以获得最佳结果）。

**参考：**

- [https://docs.openclaw.ai/concepts/models](https://docs.openclaw.ai/concepts/models)
- [https://openclaw.ai/](https://openclaw.ai/)
- [https://www.digitalocean.com/resources/articles/what-is-openclaw](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [https://medium.com/@ozbillwang/understanding-openclaw-a-comprehensive-guide-to-the-multi-channel-ai-gateway-ad8857cd1121](https://medium.com/@ozbillwang/understanding-openclaw-a-comprehensive-guide-to-the-multi-channel-ai-gateway-ad8857cd1121)
- [https://www.analyticsvidhya.com/blog/2026/03/openclaw-vs-claude-code](https://www.analyticsvidhya.com/blog/2026/03/openclaw-vs-claude-code)
