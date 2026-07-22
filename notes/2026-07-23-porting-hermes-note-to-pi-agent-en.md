---
audio: false
generated: true
image: false
lang: en
layout: post
title: Porting Hermes Note to Pi Agent
translated: false
type: note
---

Here's a summary of what we did:

## Summary

**1. Explored the project** — You showed me the current working directory (`/mnt/data/zz`), which is a **machine learning data pipeline** for downloading, extracting, tokenizing, and analyzing large datasets (FineWeb, Wikimedia, etc.) for model training.

**2. Studied the Pi Agent extension API** — You shared your Hermes `note` plugin (a Python plugin that enqueues assistant responses via `/note`), and I read the full Pi Agent docs on extensions — including `extensions.md`, `session-format.md`, and several examples (`bookmark.ts`, `summarize.ts`).

**3. Built a Pi Agent note extension** — I wrote an equivalent **TypeScript extension** at `~/.pi/agent/extensions/note/index.ts` that:

- Registers a `/note` command
- Grabs the last (or Nth) assistant response from the session via `ctx.sessionManager.getEntries()`
- Strips thinking/reasoning tags
- Appends it to `~/.config/pi/note_queue.json` as a JSON entry
- Supports `--title "..."` and optional response number arguments

**Key mapping:**
- Hermes (Python) → Pi Agent (TypeScript)
- `ctx.register_command()` → `pi.registerCommand()`
- Private `ctx._manager._cli_ref` → stable public `ctx.sessionManager.getEntries()`
- Plugin dir `~/.hermes/plugins/note/` → extension dir `~/.pi/agent/extensions/note/index.ts`