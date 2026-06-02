---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Source Leak Reimplementations
translated: false
type: note
---

**Question:** What are the best Claude Code open source projects/reimplementations right now?

**Answer:**

Big story here: on **March 31, 2026**, Anthropic accidentally shipped source maps inside the Claude Code npm package, exposing the full TypeScript source (~1,884 files). Chaofan Shou discovered that the source map files embedded in the published npm package contained the original TypeScript source under the `sourcesContent` key in the JSON. This triggered an explosion of reimplementations. Here's the landscape:

---

## The Leaked Source

**[yasasbanukaofficial/claude-code](https://github.com/yasasbanukaofficial/claude-code)**
The raw leaked TypeScript source — the actual Claude Code CLI codebase including tool-calling, agentic workflows, and terminal UI. Archived for educational purposes. Note: this is just the skeleton, not the model/brain.

**[chauncygu/collection-claude-code-source-code](https://github.com/chauncygu/collection-claude-code-source-code)**
A collection hub that archives the raw leaked TypeScript source and houses multiple subprojects studying Claude Code from multiple angles — architecture analysis, research reports, and clean-room reimplementations.

---

## Best Reimplementations

### 1. `nano-claude-code` (Python) — Best for learning internals

A minimal, fully-runnable Python reimplementation that has grown from a ~900-line v1.0 prototype to a ~5,000-line v3.0 with multi-agent orchestration, persistent memory, and a skill system. Unlike architectural studies, it's a real coding assistant you can use immediately. Supports 20+ models: Anthropic, OpenAI, Gemini, DeepSeek, Ollama, LM Studio.

Tool coverage: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, MemorySave/Delete/Search, Agent, SendMessage, Skill, SkillList — plus built-in `/commit`, `/review`, and custom markdown skills with argument substitution and fork/inline execution.

**This is the best one to study if you want to understand the agent loop architecture.**

### 2. `ruvnet/open-claude-code` (TypeScript) — Best clean-room drop-in replacement

A clean-room implementation (no leaked source used) that mirrors the actual Claude Code architecture: async generator agent loop, 25 tools, 4 MCP transports (stdio, SSE, Streamable HTTP, WebSocket), 6 permission modes, hooks, settings chain, sessions. Supports Anthropic, OpenAI, Gemini, AWS Bedrock, Google Vertex. Automated nightly releases with 903+ tests.

```bash
npx @ruvnet/open-claude-code "explain this codebase"
```

### 3. `openclaw/openclaw` — Referenced widely for architecture comparison

Mentioned in multiple analyses as the closest peer to the original. Used in cross-system comparisons alongside Claude Code and Hermes-Agent to analyze agent design principles.

---

## Trending on GitHub (claude-code topic, May 2026)

The hottest repos right now by stars:

- **"Bash is all you need"** — a nano-claude-code-like agent harness built from scratch in Python (~61.9k stars)
- **awesome-claude-skills** — curated list of skills, MCPs, and workflow automation tools (~59.6k stars)
- **omo (oh-my-opencode)** — TypeScript agent harness/TUI, previously oh-my-opencode (~43.2k stars)

---

## What to Study as an AI Engineer

| Repo | Why it matters |
|------|---------------|
| `nano-claude-code` | Clean Python agent loop — read the source top-to-bottom |
| Leaked TypeScript source | See the actual system prompts, tool schemas, self-healing mechanisms |
| `ruvnet/open-claude-code` | Production-quality clean-room; good reference for MCP transport impl |
| `VILA-Lab/Dive-into-Claude-Code` | Systematic analytical framework tracing design values → principles → implementation — good for understanding why architectural choices were made, not just what they are |

The biggest insight from the leak: cross-cutting integrative mechanisms — not modular features — are the true locus of engineering complexity in Claude Code. The tool loop, permission system, and context management all bleed into each other. Worth studying that specifically.

---

**References:**

- [chauncygu/collection-claude-code-source-code](https://github.com/chauncygu/collection-claude-code-source-code)
- [ruvnet/open-claude-code](https://github.com/ruvnet/open-claude-code)
- [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)
- [GitHub claude-code topic](https://github.com/topics/claude)
