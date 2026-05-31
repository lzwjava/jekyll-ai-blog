---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Session Caching Affects AGENTS.md Updates
translated: false
type: note
---

Here's the full picture from the code:

AGENTS.md is loaded as part of the system prompt, and the system prompt is **cached per session** — not rebuilt every turn. Here's exactly how it works:

1. **First turn of a new session** — `agent/conversation_loop.py:288` calls `agent._build_system_prompt(system_message)` which runs `agent/system_prompt.py:build_system_prompt_parts()`. That function (line 290-299) calls `build_context_files_prompt()` from `agent/prompt_builder.py:1468`, which reads AGENTS.md from disk via `_load_agents_md()` (line 1406-1419). The result is cached on `agent._cached_system_prompt`.

2. **Subsequent turns in the same session** — `conversation_loop.py:582` checks `if agent._cached_system_prompt is None`. Since it's already set, it skips the rebuild entirely and reuses the cached version verbatim. This is intentional — it keeps the Anthropic/OpenAI prefix cache warm (documented at line 571-581).

3. **Session resume (gateway path)** — The gateway creates a fresh `AIAgent` per message. `conversation_loop.py:247-271` loads the stored system prompt from the SQLite session DB instead of rebuilding. Same effect: AGENTS.md changes are NOT picked up.

4. **After context compression** — `conversation_compression.py:496` sets a new `_cached_system_prompt`, but it rebuilds from the *existing* prompt's structure, not from disk.

5. **Invalidation** — `system_prompt.py:invalidate_system_prompt()` (line 367-375) sets `_cached_system_prompt = None` and reloads memory from disk. But this is only called after compression events, not after file edits.

So the answer is: **you need to start a new session** (e.g., `/new` in the CLI, or a new conversation in the gateway) for AGENTS.md changes to take effect. Within the same session, the system prompt is frozen for prefix-cache stability. No need to restart the hermes process itself — just start a fresh session.

The one exception: if you're in the CLI and the session has never been used (no `_cached_system_prompt` yet), the very first message will pick up your edits. But once a session has started, the prompt is locked.