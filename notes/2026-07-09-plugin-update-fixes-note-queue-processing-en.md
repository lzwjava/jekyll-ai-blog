---
audio: false
generated: true
image: false
lang: en
layout: post
title: Plugin Update Fixes Note Queue Processing
translated: false
type: note
---

Fixed. The problem was the file didn't actually get updated from the queue-based rewrite — the old `create_note_from_content` code was still on disk. Now it's correct:

**What changed**: The plugin now calls `_enqueue(text, "note")` instead of `create_note_from_content()` + `gitmessageai()`. The `ww note watch` daemon (pid 133147, already running) picks up new entries automatically.

**Verification**: Queue file is at `~/.config/ww/note_queue.json` — currently empty (0 entries). When you run `/note` in a Hermes CLI session, it'll write a pending entry there, and the watcher will process it within 3 seconds.

**To test**: Start a Hermes CLI session, run any command, then `/note` — it should say "Enqueued (id=...)" and the watcher will pick it up.
