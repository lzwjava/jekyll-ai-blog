---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM-Wrap Code Clipboard Command
translated: false
type: note
---

Done. Here's what was implemented:

**3 files changed:**

1. `ww/note/create_note_utils.py` — Added `wrap_code_snippets(content)` function that calls LLM to wrap code in triple-backtick markdown fences with language hints. Non-code content stays untouched.

2. `ww/note/note_queue.py` — Updated `enqueue_clipboard()` to accept optional `text` and `code` parameters. When `code=True`, stores `"code": true` in the queue entry.

3. `ww/main.py` — Added `--code` flag handling in the `note` command:
   - Reads clipboard → calls `wrap_code_snippets()` LLM → enqueues with `code=True`
   - Runs before duplicate check (content is wrapped at enqueue time)
   - Works with `ww note watch` since it enters the queue like any other entry

**Also updated:**

- Help text: `ww note --code            LLM-wrap code in clipboard, then queue`
- Zsh completions: `--code` and `--sync` flags for `ww note`

**Flow:**

```
ww note --code
  → clipboard read
  → LLM wraps code in ``` fences
  → enqueue (with code=true flag)
  → ww note watch consumes it → creates note → commit → push
```
