---
audio: false
generated: true
image: false
lang: en
layout: post
title: Queue-Based Note Processing Architecture
translated: false
type: note
---

Done. Here's the corrected architecture:

---

## Note Plugin — Queue-Based Architecture

**What changed**: The `/note` slash command no longer processes the response directly. Instead it **enqueues** the text content, and the separate `ww note watch` daemon picks it up.

**Flow**:
```
/note  (Hermes CLI)
  └→ enqueue text → ~/.config/ww/note_queue.json
                        │
            ┌───────────┴───────────┐
            │                       │
   ww note watch              cron: every 30m
   (daemon, polls 3s)        (safety net)
            │                       │
            └───────────┬───────────┘
                        ↓
               ww note process
                  ├─ LLM title gen
                  ├─ write markdown file
                  ├─ fix MathJax + tables
                  ├─ git commit + push
                  └─ clear done from queue
```

**What's running**:
- `ww note watch` — daemon pid **133147** (started Jul 3, still active)
- Hermes cron `ww-note-process` — every 30m as safety net if daemon dies

**Plugin** (`~/.hermes/plugins/note/__init__.py`):
- `/note` → `_enqueue(text, "note")` → writes to `~/.config/ww/note_queue.json`
- `/note 3` → enqueues 3rd response back
- `/note --title "Foo"` → stores title hint in queue entry
- No LLM calls, no file writes, no git in the plugin itself — just fast enqueue

**Dependencies**: `ww` package installed in Hermes venv, `pyperclip` also installed.