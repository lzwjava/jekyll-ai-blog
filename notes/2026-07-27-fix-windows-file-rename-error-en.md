---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Windows file rename error
translated: false
type: note
---

**Summary of the fix:**

- **Root cause**: `tmp.rename(qf)` uses `os.rename()` under the hood, which on **Windows** refuses to overwrite an existing file (raising `FileExistsError`). On POSIX (macOS/Linux), `rename()` atomically replaces the target — but not on Windows.
- **Fix**: Replaced `tmp.rename(qf)` with `os.replace(tmp, qf)`. The `os.replace()` function is explicitly designed as the cross-platform equivalent — it atomically replaces the destination file on both POSIX **and** Windows.
- Also added the `import os` statement that was missing.

You can now run `uv run ww note process` again — the `mark_done` → `_save_queue` path should work on Windows without the `FileExistsError`.
