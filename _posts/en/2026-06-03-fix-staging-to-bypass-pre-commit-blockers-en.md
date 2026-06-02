---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix staging to bypass pre-commit blockers
translated: false
type: note
---

Done. Here's what was changed and why:

**Root cause:** `gitmessageai()` did `git add -A` which stages ALL files in the repo. When pre-commit runs on `git commit`, it checks every staged file — if any unrelated file fails a hook, the commit dies.

**Fix — 3 files changed:**

1. `ww/github/gitmessageai.py` — added `files` parameter. When provided, only stages those files (`git add <file1> <file2>...`) instead of `git add -A`. Falls back to `add -A` when `files=None` (backward compatible).

2. `ww/note/note_workflow.py` — passes `[created_path]` to `gitmessageai(files=...)` so only the new note gets staged and committed.

3. `ww/note/note_queue_process.py` — same fix: `_git_commit_push(files=created_paths)` passes the list of created note files through to `gitmessageai`.

**Before:** `git add -A` → pre-commit runs on ALL repo files → fails on unrelated files
**After:** `git add notes/2026-06-03-foo.md` → pre-commit runs only on the note → clean commit

All other callers of `gitmessageai` (like `ww git commit`) still get `files=None` → `git add -A`, so no behavior change elsewhere.
