---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reviewable Agent IDE ORG-II
translated: false
type: note
---

**Question:** What is the GitHub repo `yorgai/ORG2`?

**Answer:**

ORG-II is an open-source, Cursor-style agent IDE built on a fundamentally different philosophy: **reviewability and control over raw coding speed**.

Key differentiators from Cursor/Claude Code:

**Architecture**

- Built with **Rust + Tauri** — local-first, <100MB on disk
- TypeScript (54%) + Rust (39%) split: frontend in TS, agent runtime in Rust
- Uses your existing API keys (no new subscription)

**The core insight it's exploring** — Cursor/Claude Code treat agents as "outsourced assistants": useful for output, black-box for audit. ORG-II treats agents as **persistent, observable colleagues** in a structured org:

- **Agent trajectory livestream + replay** — every agent session is replayable. You can audit exactly what the agent did, step by step. "AI blame" (like `git blame` but for agent actions)
- **Cross-session memory + cross-agent knowledge sharing** — agents accumulate context across sessions, not stateless per-chat
- **Long-running + scheduled sessions** — agents can run overnight, auto-restart, react to CPU/RAM availability
- **GUI, CLI, terminal, Git, browser, LSP, database tooling** all integrated
- **Browser Use + Computer Use** via native sidecars (`agent-browser`, `peekaboo` on macOS)

**Status:** v1.0.1.21, released June 20, 2026. 737 stars, AGPL-3.0.

**Why it matters to you:** This is philosophically aligned with what you'd build — it's agent-architecture-first, not LLM-wrapper-on-editor. The "org-level alignment" framing (agents as colleagues with accountability, not black-box assistants) is the missing layer above what Claude Code/Cursor give you. The replayable execution traces are particularly interesting for debugging agent failures, which is a real pain point at scale.

Worth watching if you're building CLI agents (`ww`, `zz`) and care about auditability of what the agent actually did.

References:

- [yorgai/ORG2 on GitHub](https://github.com/yorgai/ORG2)
