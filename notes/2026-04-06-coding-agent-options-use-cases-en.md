---
audio: false
generated: true
image: false
lang: en
layout: post
title: Coding Agent Options and Use Cases
translated: false
type: note
---

Based on the `coding-agent` skill, I have a few available:

- **Claude Code** — my go-to for most tasks (Anthropic's CLI, no PTY needed, just `--print --permission-mode bypassPermissions`)
- **Codex** — OpenAI's CLI, good but needs `pty:true`
- **OpenCode** / **Pi** — alternatives, also need PTY

For most coding work, I'd use **Claude Code** — it's the most straightforward since it doesn't need a PTY. For quick edits or reading code, I just use my built-in tools directly (`edit`, `read`, `exec`). I only delegate to an agent when something needs real file exploration, refactoring across many files, or building something new from scratch.

What are you looking to tackle?
