---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Harder Than What
translated: false
type: note
---

Both questions hit real pain points.

**What vs Why — "Why" is harder to trace.**

"What" leaves artifacts: tool calls are logged, files have diffs, terminal output is captured in the conversation messages. You can reconstruct the action sequence from the session DB.

"Why" is ephemeral. The model's reasoning happens in the stream — reasoning_content may be stored in the message but often isn't fully persisted, and the context that influenced a decision (why it chose approach A over B, why it picked that specific file path, why it decided to refactor before fixing) gets lost across turns, especially after `/compress`. The tool call says `write_file(path, content)` but not "I chose this structure because of what I saw 3 turns ago in that error message."

This is why Hermes saves trajectories (`save_trajectories=True`) — they capture the full message chain including tool results. But even trajectories show the model's *outputs*, not the latent reasoning that led to them.

Practical mitigation:

- Verbose tool outputs help (the "why" is sometimes in the model's text before a tool call)
- Session search can recover context around decisions
- Writing plans first (the `/plan` pattern) externalizes the "why" into a markdown file

**Interruptions mid-task — three scenarios:**

1. **User interrupts (Ctrl+C / /stop):** The agent checks `_interrupt_requested` at iteration boundaries and during streaming. In-flight API calls get their connection killed. Tool execution (e.g., a running terminal command) may complete or may be left partial. The conversation is persisted up to the last completed turn.

2. **Network/provider failure:** The retry loop handles this (as we discussed). If retries exhaust, the conversation is persisted with an error message. You can resume — the model sees the error in history and can pick up.

3. **Process crash / timeout:** The session DB (SQLite) persists messages at each turn boundary. A crash mid-turn loses that turn's work but everything before it survives. `/resume` reloads from the DB.

The real danger is **partial side effects**: a subagent writes half a file, a terminal command modifies state then the agent dies, a git commit goes through but the follow-up fix doesn't. There's no transactional rollback. This is why long tasks benefit from:

- Frequent commits (so you can `git diff` / `git stash`)
- Plans as checkpoints (`.hermes/plans/`)
- Breaking work into subagents (each is atomic-ish — succeeds or fails as a unit)
