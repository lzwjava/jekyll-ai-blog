---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenHarness Open Agent Framework
translated: false
type: note
---

Question: What is OpenHarness, the open-source project at https://github.com/HKUDS/OpenHarness?

Answer:

## OpenHarness — Open Agent Harness (`oh`)

OpenHarness is an open-source Python framework developed by the HKUDS (Hong Kong University Data Science) group. It delivers core lightweight agent infrastructure covering tool-use, skills, memory, and multi-agent coordination. The project was initially released on **April 1, 2026** as v0.1.0, and has quickly gained traction with over **5.7k stars** and **973 forks** on GitHub.

---

### What is an "Agent Harness"?

An **Agent Harness** is the complete infrastructure that wraps around an LLM to make it a functional agent. The model provides intelligence; the harness provides hands, eyes, memory, and safety boundaries.

In short:
- The **LLM** = the brain (decides *what* to do)
- The **harness** = the body (handles *how* to do it — safely, efficiently, with observability)

---

### Core Architecture

OpenHarness implements the core Agent Harness pattern with 10 subsystems:

| Subsystem | Role |
|---|---|
| `engine/` | Agent loop — stream, tool-call, loop |
| `tools/` | 43+ tools (file, shell, search, web, MCP) |
| `skills/` | On-demand knowledge loading via `.md` files |
| `plugins/` | Extensions — commands, hooks, agents, MCP servers |
| `permissions/` | Safety — multi-level modes, path rules |
| `hooks/` | Lifecycle events (PreToolUse / PostToolUse) |
| `commands/` | 54 slash-commands (`/help`, `/commit`, `/plan`, etc.) |
| `memory/` | Persistent cross-session knowledge via `MEMORY.md` |
| `coordinator/` | Multi-agent subagent spawning and team coordination |
| `ui/` | React-based Terminal UI (TUI) |

---

### Key Features

#### 1. Agent Loop Engine
The Agent Loop supports streaming tool-call cycles, API retry with exponential backoff, parallel tool execution, and token counting & cost tracking.

#### 2. Tools (43+)
Tools span multiple categories: File I/O (Bash, Read, Write, Edit, Glob, Grep), Search (WebFetch, WebSearch, ToolSearch), Agent tools for subagent spawning, Task management, and MCP (Model Context Protocol) integration. Every tool has Pydantic input validation, self-describing JSON Schema, permission integration, and hook support.

#### 3. Skills System
Skills are on-demand knowledge loaded only when the model needs them. Examples include `commit`, `review`, `debug`, `plan`, `test`, `simplify`, `pdf`, `xlsx`, and 40+ more. It is also compatible with the official `anthropics/skills` repo — just copy `.md` files to `~/.openharness/skills/`.

#### 4. Permissions & Safety
Multi-level permission modes are supported: **Default** (ask before write/execute), **Auto** (allow everything, for sandboxed environments), and **Plan Mode** (block all writes for review-first workflows). Path-level rules and denied command lists can be configured in `settings.json`.

#### 5. Multi-Agent / Swarm Coordination
OpenHarness supports subagent spawning and delegation, team registry and task management, background task lifecycle management, and ClawTeam integration (on the roadmap).

#### 6. Plugin System
Compatible with claude-code plugins, tested with 12 official plugins. Examples include `commit-commands` for git workflows, `security-guidance` for security warnings on file edits, `code-review` for multi-agent PR review, and `hookify` for creating custom behavior hooks.

---

### Provider Compatibility

OpenHarness supports three API formats: **Anthropic** (default), **OpenAI-compatible** (`--api-format openai`), and **GitHub Copilot** (`--api-format copilot`).

Supported providers via OpenAI format include DeepSeek, Alibaba DashScope, OpenAI, GitHub Models, SiliconFlow, Groq, and local Ollama. GitHub Copilot support uses OAuth device flow — no API keys needed.

---

### Quick Start

```bash
# One-click install
curl -fsSL https://raw.githubusercontent.com/HKUDS/OpenHarness/main/scripts/install.sh | bash

# One-command demo
ANTHROPIC_API_KEY=your_key uv run oh -p "Inspect this repository and list the top 3 refactors"

# Interactive mode
oh

# Non-interactive / scripting
oh -p "List all functions in main.py" --output-format json
```

---

### Who Is It For?

OpenHarness is designed for researchers, builders, and the community who want to: understand how production AI agents work under the hood, experiment with cutting-edge tools, skills, and agent coordination patterns, extend the harness with custom plugins, providers, and domain knowledge, and build specialized agents on top of proven architecture.

---

### Tech Stack

- **Backend**: Python ≥ 3.10, managed with `uv`
- **Frontend TUI**: React + Ink (Node.js ≥ 18)
- **License**: MIT

References:

- [https://github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness)