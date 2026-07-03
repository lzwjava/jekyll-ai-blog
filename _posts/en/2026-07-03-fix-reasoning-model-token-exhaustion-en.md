---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix reasoning model token exhaustion
translated: false
type: note
---

Two changes applied. Here's the summary:

**Root cause**: `deepseek/deepseek-v4-flash` is a reasoning model. It outputs chain-of-thought in a `reasoning` field before producing the actual `content`. When `content` is `null` and `finish_reason` is `"length"`, the model exhausted its token budget during reasoning and never emitted the answer.

**Fixes** (both files in `/home/xiaoxin/projects/ww/`):

1. **`ww/llm/openrouter_client.py`** — when `content` is null, fall back to the `reasoning` field instead of crashing. A warning is printed so you know it happened, but the note gets created.

2. **`ww/note/create_note_utils.py`** — bumped `max_tokens` for title generation from 1024 → 4096, giving reasoning models enough room to both think (reasoning) and produce the 6-word title (content) without exhausting the budget.

If the watcher/processor is already running, you'll need to restart it for the changes to take effect (`Ctrl+C` the watcher, then `ww note watch` again).