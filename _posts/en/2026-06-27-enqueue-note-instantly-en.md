---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enqueue Note Instantly
translated: false
type: note
---

Done. Here's what changed:

`/Users/lzwjava/.hermes/plugins/note/__init__.py` — `/note` now enqueues instead of running the full pipeline. It's instant (just writes to `~/.config/ww/note_queue.json`), no LLM call, no git inline.

Before: LLM title gen → file write → git add → commit → push (slow, fails on pre-commit hooks)
After: read response → write JSON → done (< 1 second)

To auto-drain the queue, you have two options:

1. Background watcher: `ww note watch` (watches queue file, processes on change)
2. System crontab (your preference): run `ww note process` periodically

Want me to add a system crontab entry to process the queue every few minutes?
