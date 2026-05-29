---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Agentic Coding Tool
translated: false
type: note
---

**Question:** What is https://claude.com/product/claude-code?

**Answer:**

That's the official product page for **Claude Code** — Anthropic's agentic coding tool. Here's the TL;DR relevant to you:

**What it is:** A terminal-first AI coding agent that operates directly in your codebase. Not a chat assistant — it's an agent that reads files, runs commands, writes code, and opens PRs autonomously.

**Install:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Where it runs:**
- Terminal (primary)
- VS Code / JetBrains IDE extensions
- Desktop app (parallel task management, visual diffs)
- Web (`claude.ai/code`)
- Slack (kick off tasks, get PRs back)
- Mobile → delegates to your local machine (research preview)

**Key capabilities:**
- Agentic codebase search — no manual context file selection, it figures out the relevant code itself
- Multi-file coordinated edits
- Full GitHub/GitLab workflow: reads issues → writes code → runs tests → opens PR
- Runs your test suites and build systems
- Configurable via `CLAUDE.md` files; also scriptable via SDK or GitHub Actions

**Models it uses:** Sonnet 4.6 and Opus 4.7 (per the pricing table on the page — note Opus 4.7 appears to be a newer model listed here).

**Pricing:**
- Included in **Pro** ($17/mo) — limited usage, small codebases
- **Max 5x** ($100/mo) — everyday use in larger codebases
- **Max 20x** ($200/mo) — power user tier

**Recent notable features (2026):**
- **Routines** — schedule tasks, trigger via API or events (April 2026)
- **Auto mode** — safer long-running alternative to `--dangerously-skip-permissions` (March 2026)
- Redesigned desktop app for parallel task management (April 2026)

**For you specifically:** Given your terminal-first workflow and AI engineering trajectory, Claude Code is the direct competitor/complement to your custom CLI agents (`ww`, `zz`, etc.). It's worth running it on your MacBook Air for day-to-day coding tasks. The interesting angle for you is studying how it handles agentic loops — it's a production-grade example of the tool-use + planning architectures you're building toward. The `CLAUDE.md` configuration system is also worth exploring for project-level context injection.

**References:**

- [Claude Code product page](https://claude.com/product/claude-code)
- [Claude Code documentation](https://code.claude.com/docs/en/overview)
- [Introduction to agentic coding](https://claude.com/blog/introduction-to-agentic-coding)