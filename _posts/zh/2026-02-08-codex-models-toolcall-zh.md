---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 最适合工具调用的 Codex 模型
translated: true
type: note
---

我将搜索有关 OpenAI Codex 的信息，以及哪些模型最适合 tool calling。根据搜索结果，以下是用于 tool calling 的最佳 OpenAI Codex 模型：

## Top Models for Tool Calling in Codex

**GPT-5.2-Codex** 专门针对可靠 cross-tool calling 进行了优化，具有更高的准确性和更好的 long-context 理解能力。它提供可靠的 tool calling 功能，使其在处理长时间运行的 coding 任务时成为更值得信赖的伙伴，同时在推理过程中保持较高的 token 效率。

**GPT-5.3-Codex** 是用于 tool-using 工作流的最新且最强大的 agentic coding 模型。它结合了前沿的 coding 性能和更强的 reasoning 能力，为 Codex 用户提升了 25% 的运行速度。

**GPT-5-Codex-Mini** 是一项更轻量、更具成本效益的选择，在维持良好的 tool-calling 能力的同时，作为 ChatGPT 订阅的一部分，它提供约 4 倍的使用额度。

## Custom Provider Configuration

Codex 配合推荐模型使用效果最佳，但你也可以在 config.toml 配置文件中将 Codex 指向任何支持 Chat Completions 或 Responses API 的模型和 provider，以适应你的特定使用场景。

对于 config.toml 中的自定义 provider 设置，建议指定一个支持 **Responses API**（首选）或 Chat Completions API 的模型，并优先选择专为 agentic 工作设计且具有强 tool-calling 能力的模型。

需要我帮你配置 config.toml 文件中的特定模型吗？
