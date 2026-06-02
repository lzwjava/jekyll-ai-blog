---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Working Directory Affects Hermes
translated: false
type: note
---

Good question. Here's how working directory actually affects Hermes:

**The mechanism: `TERMINAL_CWD`**

When you launch `hermes` from a directory, that directory becomes `TERMINAL_CWD` — an env var that every tool reads. It's the base for:

1. **Terminal commands** — `bash` commands run with `cwd=TERMINAL_CWD` (terminal_tool.py:1033)
2. **File operations** — `read_file`, `write_file`, `search_files` resolve relative paths against it (file_tools.py:122-126)
3. **execute_code** — Python scripts run in `TERMINAL_CWD` by default (code_execution_tool.py:1230)
4. **Context files** — AGENTS.md, CLAUDE.md, .cursorrules loaded from cwd
5. **Subagent delegation** — child agents inherit the parent's cwd

**For search/grep specifically:**

The `search_files` tool uses ripgrep (`rg`). When you pass a relative path like `.` or `src/`, it resolves against `TERMINAL_CWD`. When you pass an absolute path, it searches that directly. Ripgrep is extremely fast (~10x faster than grep), so the directory size barely matters for normal project sizes. A 100K-file monorepo still searches in milliseconds.

**The real impacts are:**

- **Context loading** — This is the big one. If you launch from `/Users/lzwjava/projects/hermes-agent`, it loads that project's AGENTS.md. If you launch from `~/projects/ww`, it loads ww's context. Different cwd = different system prompt context.
- **Relative path resolution** — All relative paths in tool calls resolve from cwd. `read_file("src/foo.py")` means different things from different directories.
- **Project-scoped venv** — `execute_code` in `project` mode uses the venv from cwd, so you get different Python packages depending on where you launched.

**Does it slow things down?**

No meaningful impact on grep/search speed. Ripgrep is I/O-bound and blazing fast. The only scenario where cwd matters for performance is if you accidentally launch from `$HOME` or `/` — then `search_files` with a relative path could traverse your entire filesystem. But that's a user error, not a Hermes design issue.

**TL;DR:** Cwd affects *what context and paths* Hermes works with, not *how fast* it runs. Launch from your project root and everything is fine.
