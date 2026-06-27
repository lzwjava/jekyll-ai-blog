---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deferred Note Processing Fix
translated: false
type: note
---

Here's what happened:

**Problem:** `/note` in Hermes ran the full pipeline synchronously — LLM title generation, file creation, git commit + push. This is slow (~10-30s) and fragile (pre-commit hooks like `end-of-file-fixer` modify files, causing the commit to fail).

**Fix:** Updated `/Users/lzwjava/.hermes/plugins/note/__init__.py` — the `/note` plugin now just enqueues content to `~/.config/ww/note_queue.json` (instant, <1s). Same pattern as `ww note`.

**Processing:** Deferred to `ww note process`, which the `ww note watch` background watcher auto-drains. No watcher or cron is currently running — the queue will accumulate until you either:

- Run `ww note watch` in a terminal
- Add a system crontab entry (`*/5 * * * * ww note process`)
- Run `ww note process` manually
