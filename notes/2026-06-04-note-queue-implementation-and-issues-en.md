---
audio: false
generated: true
image: false
lang: en
layout: post
title: Note Queue Implementation and Issues
translated: false
type: note
---

OK, I've read all the note code. Here's what's actually there:

**The note module has TWO paths:**

1. **`ww note`** (no flags) → `enqueue_clipboard()` — reads clipboard, adds to `~/.config/ww/note_queue.json`, returns instantly. This IS the queued path.

2. **`ww note --sync`** → `note_workflow.main()` — the OLD path: check uncommitted, pull, create note, fix mathjax, commit+push, open browser. This is NOT queued — it's a full synchronous pipeline.

**Queue processing:**

- `ww note process` → drains pending entries from queue, creates notes, commits+pushes
- `ww note watch` → background daemon that polls the queue file every 2s and auto-processes

**Current state:** Queue file exists at `~/.config/ww/note_queue.json` and is empty (`[]`).

So the queue IS implemented in code. What specifically are you saying isn't working? Is it:

1. `ww note` doesn't actually enqueue (clipboard read fails, or it falls through to the old path)?
2. The watcher isn't running so queued notes never get processed?
3. The summary doc is wrong about something specific?
4. Something else?

Can you clarify what behavior you're seeing vs what you expect?
