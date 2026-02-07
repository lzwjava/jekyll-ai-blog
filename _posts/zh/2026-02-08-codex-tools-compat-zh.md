---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: Codex 工具的兼容性问题
translated: true
type: note
---

我将搜索有关 Kimi-k2.5 和 Gemini Flash 与 Codex 的兼容性及其 tool calling 能力的信息。现在让我搜索 Gemini Flash 与 Codex 的兼容性：

## 是的，两者在 Codex 中都存在已知问题：

### **Kimi-K2.5 问题：**

通过 Kimi Code Subscription 使用时，Kimi K2.5 的 tool calls 存在损坏。GitHub 上有多个 issue 报告称，尽管尝试了修复，该模型仍无法使用任何 tool calls。

然而，好消息是：Kimi K2.5 提供了 OpenAI/Anthropic 兼容的 APIs，且 Kimi API 旨在兼容具有强大 agentic tool calling 支持的 chat-completions 风格工作流。

**成本考量：** Kimi K2.5 会生成大量的 reasoning tokens，且每个任务最多可执行 1,500 次 tool calls。但其 output tokens 成本约为每百万个 $3.00，而 input 成本为 $0.50-$0.60，这使得其每个 output token 的价格比某些竞争对手贵 10 倍。

### **Gemini Flash 问题：**

与 Codex 存在多个兼容性问题：

1. Gemini 3 Pro 在多轮 tool calls 中失败，因为 thought_signature 无法通过 OpenAI 兼容层保留。

2. Gemini 2.5 Flash 的多轮 function calling 失败并伴有验证错误：“function response parts must equal function call parts”，因为 assistant 消息在每个 tool call 中获得 2 个部分（thought signature + function call），而 tool response 消息仅获得 1 个部分。

3. 在某些环境中，Gemini 2.5 模型始终因不明原因无法调用 tools，而之前的 Gemini 2.0 可以正常执行 tools。

4. 尽管 Gemini 1.5-pro 在相同配置下运行良好，但 Gemini 1.5-flash 的 function calling 无法工作。

## 我的建议：

对于你在 Codex 中**确实能稳定工作**的较便宜选项的自定义 provider config.toml 配置：
- **GPT-4o Mini**（最安全，已验证）
- **GPT-4.1 Mini**（更好的 performance）
- **o3-Mini**（最便宜的 reasoning）

在这些兼容性问题解决之前，请避免在 Codex tool calling 中使用 Gemini Flash 和 Kimi-K2.5。