---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transient Git Status Check Error Debug
translated: false
type: note
---

You're right — the check runs against the `BASE_PATH` from `.env`.

**The directory:** `/Users/lzwjava/projects/jekyll-ai-blog`

**Code path:**

```
note_queue_process.py:process_queue()
  → _check_uncommitted()
    → check_uncommitted_changes()  (note_workflow.py:25)
      → _git_toplevel()
        → get_base_path()  →  reads BASE_PATH env var
        → git -C /Users/lzwjava/projects/jekyll-ai-blog rev-parse --show-toplevel
      → git -C <toplevel> status --porcelain
```

Right now that repo is clean:

```
$ git -C /Users/lzwjava/projects/jekyll-ai-blog status --porcelain
(empty)
```

So the error was transient — when the watcher ran `process_queue()` the second time, the blog repo had dirty state at that moment (likely from the first `process_queue` call's `_git_pull_rebase()` or from a previous `gitmessageai` commit that left something staged/dirty).

The key issue: the first `process_queue()` run found no uncommitted changes, created a note (failed as duplicate), did NOT commit (no `created_paths`), but it DID call `_git_pull_rebase()`. If that rebase hit a conflict or left `.git/REBASE_HEAD` or similar state, the second run's `check_uncommitted_changes()` would see it.

If this keeps happening, you could add debug output right before the check to see what `git status --porcelain` actually reports:

```python
# In check_uncommitted_changes(), after line 34:
if result.stdout.strip():
    print(f"[debug] git status output: {result.stdout!r}")  # ADD THIS
```