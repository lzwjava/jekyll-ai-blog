---
audio: false
generated: true
image: false
lang: en
layout: post
title: Plugin Thin Bridge to Queue
translated: false
type: note
---

Done. Here's what changed:

**Before** (v1.0.0): `/note` directly imported `ww.note.create_note_from_clipboard` and `ww.github.gitmessageai`, generated title via LLM, created the note file, ran pre-commit, git committed + pushed — all inline in the plugin.

**After** (v2.0.0): `/note` does 3 things:
1. Extracts assistant response text, strips reasoning tags
2. Copies it to clipboard (`pbcopy`/`xclip`)
3. Runs `ww note` (subprocess) which reads clipboard → queues to `~/.config/ww/note_queue.json`
4. Checks if `ww note watch` is running (via PID file), warns if not

The actual note creation, LLM title generation, git commit+push are all handled by `ww note watch` in the background. The plugin is now a thin clipboard→queue bridge.

Files modified:
- `/Users/lzwjava/.hermes/plugins/note/__init__.py` — rewrote from 191 to 176 lines, removed all `ww` internal imports
- `/Users/lzwjava/.hermes/plugins/note/plugin.yaml` — bumped to v2.0.0, updated description

Make sure `ww note watch` is running in a background terminal for notes to get processed.
