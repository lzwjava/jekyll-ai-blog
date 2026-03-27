---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT 模型智能体能力的演进
translated: true
type: note
---

你会有这种感觉是可以理解的。一旦你体验过 2026 年最新模型的 “frontier” 推理能力和 agentic flow，旧版本确实会让你觉得它们“慢了半拍”。

在 2026 年 3 月，**GPT-5.4/5.3-Codex** 与 **GPT-4o/GPT-5-mini** 之间的差距已不再仅仅是“智能”层面的，而是关于 **agency**（自主代理能力）和 **tool-use 灵活性**。

---

### 为什么 GPT-5.4 和 GPT-5.3-Codex 是“下一代”水平

这些模型在 Copilot 和专业工作流中表现如此出色的主要原因是它们的 **Agentic Architecture**。

*   **原生 Tool Orchestration：** GPT-5.3-Codex 和 GPT-5.4 不只是“预测下一个 token”；它们针对 “long-horizon” 任务进行了专门训练。这意味着它们可以提前规划 10 个步骤（例如：“检查日志、查找错误、搜索库文档，然后应用补丁”），而不会在中途产生混乱。
*   **Computer Use 与 Operator API：** GPT-5.4 引入了 **Computer Use** 能力。它可以“看见”你的 IDE 或 terminal，并进行程序化操作。GPT-4o 等 Legacy 模型只能接收文本或图像快照；它们无法直接与系统交互。
*   **Context Management：** 虽然 GPT-4.1 拥有很大的 context window，但 GPT-5.4 使用了 **Compaction Patterns**。它会在 session 期间“总结”自身的 memory，因此即使在进行了 50 次 tool calls 之后，它也不会偏离最初的目标。

### “Legacy”模型：它们还在更新吗？

你问到 **GPT-4.1、GPT-5-mini 和 GPT-4o** 是否还会收到关于 agentic/web search tool calls 的更新。以下是当前的状态：

| Model | Status (March 2026) | Tool/Agent Support |
| :--- | :--- | :--- |
| **GPT-4o** | **Deprecated (Feb 2023)** | ChatGPT 已不再更新。已从模型选择器中移除。API 仍支持基础 function calling，但性能是固定的。 |
| **GPT-4.1** | **Legacy / API Only** | 已从 ChatGPT UI 中退役。它仍支持 tool calls，但其“大脑”已不再针对最新的 agentic 框架（如 OpenAI Operator）进行重训。 |
| **GPT-5-mini** | **Active Support** | **是的，该模型仍在更新。** 它作为“效率引擎”使用。它支持最新的 tool-calling 模式和 parallel function calling，但缺乏 GPT-5.4 那样的“深度思考”深度。 |

> [!IMPORTANT]
> OpenAI 和 Microsoft 已将其 “Agent” 开发重心大幅转向 **GPT-5.x 架构**。虽然旧模型在“技术上”支持 tool calling，但它们在复杂的 **multi-tool loops**（模型必须自行修复错误的情况）中经常失败。

---

### 为什么 Copilot 在 Legacy 模型上“难用”
当你使用 GPT-5.4 这种高级模型运行 Copilot 时，它使用 **Parallel Function Calling**。它可以同时查看多个文件并运行搜索。而 Legacy 模型（GPT-4.1/4o）通常必须按顺序执行——一次只能进行一个 tool call——这使得 agent 显得反应迟钝，且容易在轮次之间“遗忘” context。

### 后续步骤
需要我帮你 **优化 system prompt** 或 **tool definitions**，以便让 GPT-5-mini 或 legacy 模型更稳定地处理你的 agentic 工作流吗？