---
audio: false
generated: true
image: false
lang: en
layout: post
title: Private Note Implementation Summary
translated: false
type: note
---

All changes work correctly. Here's a summary of what was implemented:

## Changes Summary

### 1. `ww/note/note_queue.py` — `enqueue_clipboard()` accepts `private` param
- Added `private=False` parameter
- When `True`, stores `{"private": True}` in the queue entry's extra dict

### 2. `ww/note/note_queue_process.py` — Private note processing
- Added `PRIVATE_NOTES_DIR = "/Users/lzwjava/projects/jekyll-ai-blog/private-note"`
- When processing a queue entry with `"private": True`, creates the note in `PRIVATE_NOTES_DIR` (via `create_note_from_content(content, directory=...)`)
- Private notes are **excluded** from `created_paths` so they don't get git committed/pushed
- All other processing (MathJax fix, table fix) remains the same

### 3. `ww/note/note_workflow.py` — `--private` support for `--sync` path
- Added `PRIVATE_NOTES_DIR` constant
- Added `--private` to argparse
- When `--private` is set, skips `check_uncommitted_changes()`, `git_pull_rebase()`, and the git commit/push — just creates the note in the private directory

### 4. `ww/main.py` — Route `--private` flag
- **Fast path** (`ww note --private`): Detects `--private` in `sys.argv`, removes it, passes `private=True` to `enqueue_clipboard()`
- **Sync path** (`ww note --private --sync`): Leaves `--private` in `sys.argv` for `note_workflow.py`'s argparse to handle
- Added help text: `ww note --private`

### 5. `~/.zsh/completions/_ww` — Tab completion
- Added `'--private[Save to private-notes dir, skip git push]'` to the `note)` arg completions
