---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Context Files and System Prompt
translated: false
type: note
---

Yes. Pi loads **`AGENTS.md`** (or `CLAUDE.md`) as context files every session. From the README's **Context Files** section:

> Pi loads `AGENTS.md` (or `CLAUDE.md`) at startup from:
> - `~/.pi/agent/AGENTS.md` (global)
> - Parent directories (walking up from cwd)
> - Current directory

All matching files are found by walking up from cwd, then concatenated and injected into the system prompt. For this project at `/home/lzw/projects/pi`, the file `AGENTS.md` in the repo root is what I loaded and am following as project rules.

You can also see which AGENTS.md files are loaded in the interactive startup header. Disable loading with `--no-context-files` / `-nc`.

There's also **`SYSTEM.md`** for replacing the system prompt entirely (`.pi/SYSTEM.md` or `~/.pi/agent/SYSTEM.md`), and **`APPEND_SYSTEM.md`** for appending without replacing.