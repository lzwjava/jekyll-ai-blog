---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端与基于 Web 的 AI 编程
translated: true
type: note
---

Question: What is the key behavioral difference between terminal-based AI coding tools (like Claude Code) and web-based chatbots when handling general knowledge questions, and how does this affect efficiency?

Answer:

## The "Wrong Tool for the Job" Problem

You've identified a real and important pain point. Terminal-based coding assistants are **context-anchored to your local project**，这意味着它们默认会从这个视角来处理几乎所有的查询——即使查询内容完全无关。

---

## Why This Happens

Terminal 编码工具（如 Claude Code）在系统 Prompt 下运行，其核心逻辑通常是：

> "You are a coding assistant working inside a local project. Use available tools (file reads, shell commands, directory listings) to understand context before answering."

所以当你询问 **"Who is Sam Altman?"** 时，它并不会直接回答，而是：

1. 可能会扫描你的项目文件寻找相关提及
2. 检查目录结构以确认相关性
3. 甚至可能运行 Shell Commands 来收集上下文
4. **然后**才给出答案——这带来了延迟并浪费了 Tokens

这就是针对非编程查询时的 **agentic reflex**（代理反应）起到了反作用。

---

## The OpenClaw Comparison

你说得对，像 **OpenClaw**（以及类似的本地 AI Assistant 封装工具）处理这种边界时通常更优雅，因为：

- 它们**并非完全锁定在项目作用域（project-scoped）内**——它们的定位更接近具有可选本地文件访问权限的通用 Assistant
- 它们不假设每个问题都需要解析本地上下文
- 它们将 Web/通用查询和本地项目查询视为**不同的模式（modes）**，而不是默认将所有内容都投入项目上下文模式

这使得它们在混合工作流中效率更高，例如在以下问题间切换时：

- "What does this function do?" *(需要本地上下文)*
- "Who founded Anthropic?" *(Web/通用知识，不需要本地上下文)*

---

## The Real Trade-Off Summary

| Behavior | Claude Code / Codex CLI | Web Chatbot | OpenClaw-style |
| --- | --- | --- | --- |
| General knowledge Q&A | Slow — checks local first | Fast — answers directly | Fast — routes correctly |
| Local file/project Q&A | Excellent | Can't access | Good |
| Web search | Requires explicit prompt | Built-in | Depends on config |
| Token efficiency on general Q&A | Poor | N/A (flat rate) | Better |
| Agentic coding tasks | Best | Worst | Moderate |

---

## Practical Workarounds for Claude Code

既然你不能总是在会话中切换工具，解决方法是使用**明确的路由指令（explicit routing instructions）**：

```
# Force web search
Search the web and tell me who Sam Altman is.

# Prevent unnecessary file scanning
Answer from your training knowledge only — no need to check local files.

# Scope the task explicitly
Only look at files under ./src when answering this.
```

或者更好的办法是，在你的 Claude Code 项目配置（`CLAUDE.md`）中添加一条**持久指令（persistent instruction）**：

```markdown
## Query Routing Rules
- For general knowledge questions (people, history, concepts), answer directly from training knowledge.
- Only scan local files when the question explicitly references code, this project, or local state.
- For current events, use web search tools directly without scanning local files first.
```

---

## Bottom Line

你所描述的低效其实是一个 **system prompt 设计缺陷**，而不是技术的内在限制。Coding Assistants 被过度调校为“优先检查本地上下文”，因为这对于 80% 的编码任务来说是正确的默认设置——但对于剩下的 20% 来说，这变得非常烦人。像 OpenClaw 这样的工具通过在决定调用哪些 Tools 之前先区分查询类型，能更好地处理路由启发式逻辑。
