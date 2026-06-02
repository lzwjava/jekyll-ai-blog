---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Prompt Tracking Tools Overview
translated: false
type: note
---

**Question:** Are there existing tools or projects that record all requests and responses from Claude Code (and GitHub Copilot in VS Code) for the purpose of tracking and improving prompts? And is it possible to build a custom fullstack system for this?

**Answer:**

## Overview

Yes — this space is quite mature. There are tools at every level: open-source CLI loggers, official telemetry pipelines, managed SaaS observability platforms, and purpose-built prompt management systems. Here's a structured breakdown.

---

## Part 1: Claude Code — Existing Tools & Approaches

### A. Native JSONL Transcripts (Built-in)

Claude Code automatically writes all conversation transcripts to JSONL files on disk at `~/.claude/projects/`. Every prompt, response, and tool call is stored there. This is the lowest-friction starting point for building your own system — no proxy needed.

### B. Open-Source CLI Loggers

**`claude-code-logger`** (GitHub: dreampulse/claude-code-logger)
A CLI proxy tool that intercepts all Claude Code traffic. It runs a local proxy server and you point `ANTHROPIC_BASE_URL` at it. Features include chat mode visualization, markdown rendering of AI responses, tool usage tracking, request/response body logging, and SSE (streaming) merging. This is the closest thing to what you want to build — a man-in-the-middle logger.

**`claude-code-log`** (GitHub: daaain/claude-code-log)
A Python CLI tool that converts Claude Code's JSONL transcripts into readable HTML files. It supports project hierarchy processing, session navigation, token usage tracking, date filtering, and an interactive TUI interface.

**`claude-trace`** (by Mario Zechner)
A tool that monkeypatches Claude Code's internal `fetch` to intercept all request-response pairs between the client and Anthropic's servers, writing them to a JSONL file on disk. This captures system prompts, tool definitions, and the full conversation — giving complete introspection including things not normally visible.

### C. Official OpenTelemetry (OTEL) Pipeline

Claude Code exports events via OpenTelemetry when `OTEL_LOGS_EXPORTER` is configured. Key events include `claude_code.user_prompt` (when a user submits a prompt), `claude_code.api_request` (each API call), and `claude_code.tool_result` (tool execution completions). You can set `OTEL_LOG_TOOL_DETAILS=1` to include MCP server/tool names.

The recommended open-source stack routes data through: Claude Code → OpenTelemetry Collector → Prometheus (metrics) + Loki (events/logs) → Grafana (visualization). You enable it with `CLAUDE_CODE_ENABLE_TELEMETRY=1`.

### D. Managed SaaS Options for Claude Code

**LangSmith (LangChain)**
LangSmith supports tracing Claude Code via a Stop hook that reads generated conversation transcripts, converts messages to LangSmith runs, and sends them to a project. Tracing includes user messages, tool calls, and assistant responses, enabled per-project via `TRACE_TO_LANGSMITH=true` in `.claude/settings.local.json`.

**Datadog AI Agents Console**
Datadog's AI Agents Console aggregates Claude Code performance metrics including latency percentiles, error rates, failed bash commands, and requests by repository, giving project-level insight.

**Dev-Agent-Lens (Arize)**
An open proxy-based layer that routes Claude Code requests through LiteLLM, emits OpenTelemetry and OpenInference spans, and sends them to Arize AX or Phoenix locally. It captures streaming responses, nested tool invocations, and internal calls — things that standard logs miss.

---

## Part 2: GitHub Copilot in VS Code — What's Possible

### A. Built-in Logging (Diagnostic Mode)

VS Code provides tools to inspect what happens when you send a prompt. You can set log level to `Trace` for the GitHub Copilot and GitHub Copilot Chat extensions via the Command Palette (`Developer: Set Log Level`), then view output in the Output panel. There is also an "Agent Debug" panel that shows a chronological event log of agent interactions including tool call sequences, LLM requests, token usage, prompt file discovery, and errors.

### B. The Hard Limitation

Unlike Claude Code, **Copilot does not provide an open API for capturing full request/response pairs**. Copilot routes all requests through a proprietary Copilot proxy server that handles rate limiting, authentication, and security checks before forwarding to the LLM backend. The traffic is encrypted end-to-end. This means you cannot easily intercept the raw prompts+responses without a corporate MITM proxy (e.g., Zscaler).

### C. What You CAN Track with Copilot

- **Usage quota** (requests used, token quota): via the VS Code status bar dashboard and the GitHub API endpoint `https://api.github.com/copilot_internal/user`. There is an open-source VS Code extension `copilot-usage-tracker` that tracks premium request usage in real time using VS Code's GitHub auth provider.
- **Agent session logs**: For the Copilot coding agent, you can view session logs directly in VS Code by clicking the Agent sessions panel, and see the rationale behind Copilot's commits as they happen.
- **Diagnostic log files** stored in VS Code's standard extension log location — useful for debugging but not structured for prompt improvement.

**Bottom line for Copilot**: You cannot capture raw prompt/response pairs at the individual suggestion level from VS Code. You can only track usage metrics and agent-mode session logs.

---

## Part 3: Dedicated Prompt Management Platforms (SaaS)

If your goal is specifically **prompt improvement and iteration tracking** (not just raw logging), these platforms are purpose-built for that:

| Platform | Key Strength | Open Source? |
|---|---|---|
| **PromptLayer** | Middleware layer that logs all LLM requests, enables non-technical prompt iteration, A/B testing, and version control via a visual dashboard | No |
| **Langfuse** | Open-source LLM observability with detailed tracing, cost tracking, latency monitoring, and prompt versioning | Yes |
| **LangSmith** | Excels in logging, traceability, deep insights into prompt performance, systematic debugging and optimization | No |
| **Datadog LLM Observability** | Correlates prompt versions with performance metrics — latency, token cost, error rate — across production traffic | No |
| **Lilypad** | Wraps LLM calls in Python functions, automatically versions all changes, captures full execution context so every output can be traced and reproduced | Yes |

---

## Part 4: Should You Build a Custom Fullstack System?

**Yes, it makes sense to build if:**

- You want to track Claude Code prompts **specific to your team's workflow** (e.g., tagging by project, developer, outcome quality)
- You want **prompt improvement workflows** beyond just raw logging — ratings, annotations, suggested rewrites
- You want to combine Claude Code logs with Copilot usage data in one dashboard

**Recommended architecture for building your own:**

```
Claude Code (OTEL or JSONL)
    ↓
Backend API (Node.js / FastAPI)
    ↓
Database (PostgreSQL for structured data + full-text search)
    ↓
Frontend Dashboard (Next.js)
  - View all sessions + prompts
  - Rate responses (good/bad)
  - Annotate and version prompts
  - Compare prompt versions side-by-side
  - Token/cost analytics
```

For Claude Code specifically, the easiest data source is the **`~/.claude/projects/` JSONL files** — no proxy setup needed. You can build a file-watcher backend that ingests new sessions in near-real-time.

For Copilot, you are limited to: agent session logs (for coding agent mode) + usage quota via GitHub API. Full prompt/response capture is not feasible without a corporate network proxy.

---

**References:**

- [Claude Code Official Monitoring Docs](https://code.claude.com/docs/en/monitoring-usage)
- [claude-code-logger (GitHub)](https://github.com/dreampulse/claude-code-logger)
- [claude-code-log (GitHub)](https://github.com/daaain/claude-code-log)
- [claude-trace / cchistory writeup](https://mariozechner.at/posts/2025-08-03-cchistory/)
- [Claude Code + OpenTelemetry + Grafana guide](https://quesma.com/blog/track-claude-code-usage-and-limits-with-grafana-cloud/)
- [LangSmith Claude Code Tracing](https://docs.langchain.com/langsmith/trace-claude-code)
- [Dev-Agent-Lens (Arize)](https://arize.com/blog/claude-code-observability-and-tracing-introducing-dev-agent-lens/)
- [Datadog Claude Code Monitoring](https://www.datadoghq.com/blog/claude-code-monitoring/)
- [PromptLayer](https://www.promptlayer.com/)
- [Langfuse](https://langfuse.com/)
- [Top 5 Prompt Management Platforms 2025](https://www.getmaxim.ai/articles/top-5-prompt-management-platforms-in-2025/)
- [VS Code Copilot Troubleshooting / Agent Debug](https://code.visualstudio.com/docs/copilot/troubleshooting)
- [copilot-usage-tracker (GitHub)](https://github.com/ethanhubin/copilot-usage-tracker)
- [GitHub Copilot Chat: Life of a Prompt](https://devblogs.microsoft.com/all-things-azure/github-copilot-chat-explained-the-life-of-a-prompt/)
