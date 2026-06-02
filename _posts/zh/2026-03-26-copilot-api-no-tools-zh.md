---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot API 缺少工具调用支持
translated: true
type: note
---

**Question:** 来自 https://github.com/ericc-ch/copilot-api 的 GitHub Copilot API 是否具有 tool call 能力，类似于 OpenAI 风格的 function/tool calling？

**Answer:**

不，**ericc-ch/copilot-api** 不支持原生的 tool calling 或 function calling（即，在 chat completions 中传递 `tools` 参数并让模型返回 tool calls）。

### Key Details

- 该项目是一个**非官方的反向工程 proxy**，它将 GitHub Copilot 转换为兼容 **OpenAI Chat Completions API** (`/v1/chat/completions`) 和 **Anthropic Messages API** (`/v1/messages`) 的服务器。
- 它支持基础的 chat、models 列表和 embeddings，适用于需要 OpenAI 或 Anthropic 风格后端的工具（包括支持 **Claude Code**）。
- 然而，它由于**没有**实现 `tools` / `functions` 参数，也不处理来自底层 Copilot 模型 的 tool call 响应。该 proxy 仅转发请求，但不添加 agent 风格的 tool orchestration。

### Related Context on Tool Calling

- **GitHub Copilot 本身**（在 VS Code 等 IDE 中）已在 2025 年添加了 **tool calling / function calling** 功能，使其能够智能地搜索代码、文件、debugger 状态等。这是客户端 IDE 的能力，并未通过公开 API 暴露。
- 目前**没有官方公开的 GitHub Copilot Chat API** 用于带有 tool calling 的程序化访问。官方的 Copilot REST APIs 仅限于管理任务（例如 seat licensing），而不支持 chat 或 completions。
- 一些 fork 或相关项目（例如 `@hsupu/copilot-api`）在与 Claude 配合使用时，针对 **Anthropic-style** 的 tool 结果或 server-side tools 增加了额外处理，但核心的 ericc-ch 版本和大多数配置仍缺乏完整的 OpenAI 风格 tool calling 支持。

### Alternatives for Tool Calling

如果你需要 tool/function calling：

- 使用官方的 **OpenAI**、**Anthropic**、**Groq** 或其他原生支持该功能的 provider。
- 对于基于 Copilot 的工作流，该 proxy 在简单的 chat/completions 方面表现良好，但不适用于构建依赖动态 tool use 的 agents。

简而言之，虽然 ericc-ch/copilot-api 非常适合通过熟悉的 OpenAI/Anthropic 客户端访问 Copilot，但它**并不**提供你所询问的 tool call 能力。

**References:**

- [GitHub - ericc-ch/copilot-api](https://github.com/ericc-ch/copilot-api)
