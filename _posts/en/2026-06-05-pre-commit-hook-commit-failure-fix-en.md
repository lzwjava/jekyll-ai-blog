---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pre-Commit Hook Commit Failure Fix
translated: false
type: note
---

Here's the full picture:

## The Bug

When `ww note watch` (or `ww note process`) creates a note and tries to commit it, the commit can fail if pre-commit hooks modify the file. After failure, the retry is blocked by an uncommitted-changes check, creating an unrecoverable state.

## Root Cause — Step by Step

1. `process_queue()` creates the note file, then calls `_git_commit_push(files=created_paths)`
2. Inside `gitmessageai()`, the file is staged with `git add <file>` (line 87 of gitmessageai.py)
3. The staged diff is sent to the LLM to generate a commit message
4. `git commit -m <message>` runs — pre-commit hooks fire
5. The `end-of-file-fixer` hook detects a missing trailing newline and silently fixes the file on disk
6. Now the working tree (fixed) differs from the index (original staging). Git rejects the commit:
   ```
   error: Your local changes to the following files would be overwritten by merge
   ```
7. `_git_commit_push()` raises `CalledProcessError`, which propagates up to the `except` block in `process_queue()` (line 105-108) — it prints the error and tells you to retry
8. The queue entry is already marked done and cleaned (line 115), but the file is stuck: **staged + dirty working tree**
9. On retry, `_check_uncommitted()` (line 51-55) detects the dirty state and calls `sys.exit(1)` — dead end

The core issue: `gitmessageai` does `git add` once at the top, but if hooks modify files during `git commit`, those modifications aren't re-staged. The index goes stale.

## The Fix

In `_git_commit_push()` (`note_queue_process.py` line 31), wrap the `gitmessageai()` call in a try/except:

```python
try:
    gitmessageai(...)
except subprocess.CalledProcessError:
    # Re-stage files so hook modifications are picked up
    subprocess.run([*git, "add", *files], check=True)
    # Retry once
    gitmessageai(...)
```

When the first attempt fails because hooks modified files:
- The `except` block re-runs `git add` on the same files, staging the hook-fixed versions
- The second `gitmessageai()` call sees a clean diff (or no diff if hooks were the only change), generates a commit message, and commits successfully

This is safe because:
- Only retries once (no infinite loops)
- If the second attempt also fails, the exception propagates normally
- Covers all pre-commit hooks, not just `end-of-file-fixer`
- Works for both `ww note process` and `ww note watch` (watcher calls `process_queue()`)

## Immediate Fix

Manually re-staged the stuck note and committed:
```
9478ec3f3  docs(notes): add Qwen3.6 unpacked vs hype analysis
```

The file had already been hook-fixed on disk, so the second commit passed all hooks cleanly.
