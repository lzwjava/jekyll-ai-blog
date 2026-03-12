---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenCode Architecture and Implementation Guide
translated: false
type: note
---

I'll search for information about OpenCode's architecture and implementation.**Question:** What is a comprehensive introduction to OpenCode's architecture and how is it implemented as a code assistant?

## Answer

### Overview

OpenCode is an open-source agent that helps developers write code in the terminal, IDE, or desktop, trusted by over 5 million developers monthly with over 120,000 GitHub stars and 800 contributors. It represents a different approach to AI-assisted development compared to proprietary solutions like GitHub Copilot or Claude Code.

### Architecture

OpenCode adopts a well-organized modular architecture with clearly separated core components:

The architecture consists of: cmd/ (CLI interface using Cobra command-line framework), internal/app (core app service for application logic orchestration), configuration and session management components, internal/llm (LLM integration for OpenAI, Claude, and self-hosted models), MCP and LSP protocol support, and internal/tui (terminal UI with layout and user interaction).

OpenCode uses a client/server architecture where the TUI is a separate Golang process that communicates with an HTTP server, and generates SDK client code automatically using Stainless from an OpenAPI spec for type-safe interactions.

### Core Implementation Details

**Agent System:** OpenCode comes with two built-in primary agents (Build with full tools enabled, and Plan for read-only analysis) and two built-in subagents (General for complex searches and Explore for codebase exploration), with the ability to switch between agents using the Tab key.

**Tool Registry and Execution:** OpenCode implements a carefully designed tool registry with safely read files (with binary detection and size limits) and other tools for autonomous operation. The LLM has access to powerful tools like Language Server Protocol (LSP) servers, where changes trigger textDocument/didChange notifications to the server over STDIO, with diagnostics fed back into the LLM's context via an event bus.

**Permission System:** OpenCode implements a permission system where users can approve actions once, always, or never, with the system remembering these decisions to create a personalized trust model.

**Change Tracking:** Every operation is tracked using an internal Git repository where OpenCode creates snapshots before making changes, enabling powerful undo functionality and showing users exactly what the AI changed.

**Event Bus Architecture:** At OpenCode's heart is a strongly-typed event bus where every action (from file changes to permission requests) flows through the system, enabling complex orchestration needed for autonomous operation.

### Model Flexibility

OpenCode supports over 75 different AI providers, including Claude, OpenAI, Gemini, Grok, and local models, with a model-agnostic approach that prevents developer dependence on a single provider. The model ID in OpenCode config uses the format provider/model-id, allowing different models optimized for different tasks (for example, a faster model for planning and a more capable model for implementation).

### Development Workflow

OpenCode includes a Plan mode that disables the ability to make changes and instead suggests how it will implement features, allowing developers to ask it to create plans before implementation. The development process has developers become sparring partners with the AI—they define requirements, set architectural guardrails, and review results, with manual coding increasingly becoming the exception.

### Key Advantages

Compared to other solutions, OpenCode offers terminal-native experience, protocol support for MCP and LSP with strong extensibility, unified interface for multiple LLM providers, support for custom command systems, and lightweight operation compared to IDE-integrated solutions. OpenCode does not store code or context data, allowing it to operate in privacy-sensitive environments.

---

## References

- https://opencode.ai/
- https://opencode.ai/docs/agents/
- https://github.com/opencode-ai/opencode
- https://medium.com/@gaharwar.milind/inside-opencode-how-to-build-an-ai-coding-agent-that-actually-works-28c614494f4f
- https://dev.to/wonderlab/open-source-project-of-the-day-part-4-opencode-a-powerful-ai-coding-agent-built-for-the-g05
- https://innfactory.ai/en/blog/ai-assisted-software-development-with-opencode/
- https://cefboud.com/posts/coding-agents-internals-opencode-deepdive/
- https://thenewstack.io/open-source-coding-agents-like-opencode-cline-and-aider-are-solving-a-huge-headache-for-developers/