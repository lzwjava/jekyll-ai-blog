---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot API Lacks Tool Calling Support
translated: false
type: note
---

**Question:** Does the GitHub Copilot API from https://github.com/ericc-ch/copilot-api have tool call ability, like OpenAI-style function/tool calling?

**Answer:**

No, the **ericc-ch/copilot-api** does not support native tool calling or function calling (i.e., passing a `tools` parameter in chat completions and having the model return tool calls).

### Key Details
- This project is an **unofficial reverse-engineered proxy** that turns GitHub Copilot into a server compatible with the **OpenAI Chat Completions API** (`/v1/chat/completions`) and the **Anthropic Messages API** (`/v1/messages`).
- It supports basic chat, models listing, and embeddings, making it useful for tools that expect an OpenAI- or Anthropic-style backend (including powering **Claude Code**).
- However, it does **not** implement the `tools` / `functions` parameter or handle tool call responses from the underlying Copilot models. The proxy forwards requests but does not add agent-style tool orchestration.

### Related Context on Tool Calling
- **GitHub Copilot itself** (in IDEs like VS Code) has added **tool calling / function calling** features in 2025, allowing it to intelligently search code, files, debugger state, etc. This is a client-side IDE capability, not exposed through a public API.
- There is **no official public GitHub Copilot Chat API** for programmatic access with tool calling. The official REST APIs for Copilot are limited to management tasks (e.g., seat licensing), not chat or completions.
- Some forks or related projects (e.g., `@hsupu/copilot-api`) add extra handling for **Anthropic-style** tool results or server-side tools when used with Claude, but the core ericc-ch version and most setups still lack full OpenAI-style tool calling support.

### Alternatives for Tool Calling
If you need tool/function calling:
- Use official **OpenAI**, **Anthropic**, **Groq**, or other providers that natively support it.
- For Copilot-powered workflows, the proxy works well for simple chat/completions but not for building agents that rely on dynamic tool use.

In short, while the ericc-ch/copilot-api is excellent for accessing Copilot via familiar OpenAI/Anthropic clients, it does **not** provide the tool call ability you're asking about.

**References:**
- [GitHub - ericc-ch/copilot-api](https://github.com/ericc-ch/copilot-api)
