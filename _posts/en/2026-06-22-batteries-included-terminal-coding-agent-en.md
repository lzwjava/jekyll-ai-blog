---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batteries-Included Terminal Coding Agent
translated: false
type: note
---

**Question:** What is omp.sh?

**Answer:**

`omp` (Oh My Pi) is a **batteries-included terminal coding agent** — think Claude Code but with an actual IDE wired in at the harness level. It's a fork of [Mario Zechner's Pi](https://github.com/badlogic/pi), heavily extended by [Can Bölük (can1357)](https://github.com/can1357).

It's climbed to 5.5k+ stars in months, with a 458-fork ecosystem — signals that teams want production-grade tools, not demo prompts. (As of now, one source mentions ~13.6k stars, so it's growing fast.)

---

## What makes it different from Claude Code / Cursor

Most agent harnesses give the model a Python sandbox, `str_replace`, and some grep. omp's thesis is: **the harness is the bottleneck, not the model.** It addresses five common failure modes at the architecture level:

### 1. Hash-anchored edits (hashline)

Every line carries a short content-hash anchor. The model edits by anchor instead of reproducing whitespace, and stale anchors are caught before a file is corrupted. This eliminates the whitespace / indentation wars that kill most `str_replace`-style agents. The numbers are striking: Grok Code Fast went from 6.7% → 68.3% edit success — a tenfold lift the moment the edit format stopped eating the model alive. Grok 4 Fast got -61% token output once the retry loop on bad diffs disappeared.

### 2. Real LSP integration (not just grep)

Ask for a rename and you get a rename. The call goes through `workspace/willRenameFiles`, so re-exports, barrel files, and aliased imports update before the file moves. Everything your IDE knows, the agent knows.

### 3. Real DAP debugging (not print statements)

A C binary segfaults: the agent attaches lldb, steps to the bad pointer, reads the frame. A Go service hangs: it attaches dlv and walks the goroutines. A Python process is wedged: debugpy, pause, inspect, evaluate. Built-in adapters: gdb, lldb-dap, debugpy, dlv, js-debug-adapter.

### 4. Native Rust core (no fork/exec on hot path)

~27k lines of Rust across three crates: `pi-natives`, `pi-shell`, `pi-ast`. Search, shell, AST, highlight, PTY, image decode, BPE counting — all in-process on the libuv pool. Other agents shell out to `rg`, `grep`, `find` — every call is a fork/exec round-trip. omp links the real implementations into the process.

### 5. Subagents + IRC bus

It spawns subagents that coordinate over an in-process IRC bus. The `task` tool fans out parallel subagents, optionally workspace-isolated. `/collab` puts your live session on a relay and shares a link for pair debugging.

---

## Scale

**40+ providers · 32 built-in tools · 13 LSP ops · 27 DAP ops · ~27k lines of Rust core.**

Providers include: OAuth into Claude Pro/Max, ChatGPT, Copilot, Cursor, Z.AI, and others; or drop an API key in the environment. Per-role models (default, smol, slow, plan) resolve automatically against what you're authenticated for.

---

## Stack

- **Runtime**: Bun (TypeScript packages) + Rust N-API addon
- **Package**: `@oh-my-pi/pi-coding-agent`
- **Config**: `~/.omp/agent/` — sessions as JSONL, config in `config.yml`
- **Sessions**: resume, fork, branch, share

---

## Install

```bash
npm install -g @oh-my-pi/pi-coding-agent
# or via bun
bun install -g @oh-my-pi/pi-coding-agent
```

---

## Relevance for you

Given you're building CLI agents (`ww`, `iclaw`, `zz`) and using Zed — worth noting: run omp inside Zed and you get the same agent you drive from the terminal — reading the buffer you're actually looking at, writing through the editor's save path, spawning shells in the editor's terminal.

Also: omp reads the eight agent-rules formats already on disk in their native shape — Cursor MDC, Cline `.clinerules`, Codex `AGENTS.md`, Copilot `applyTo`, and the rest. No migration script.

The Rust-native approach to agent tooling (in-process grep, AST, BPE counting) is architecturally interesting if you're thinking about building your own agent harness — the codebase is worth reading.

**References:**

- [omp.sh](https://omp.sh)
- [github.com/can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)
- [agentpedia.codes — Oh My Pi deep dive](https://agentpedia.codes/blog/oh-my-pi-terminal-coding-agent-guide)
- [explainx.ai — omp vs Claude Code](https://explainx.ai/blog/oh-my-pi-terminal-coding-agent-omp-mario-zechner-2026)
