---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add autostash to git pull rebase
translated: false
type: note
---

Fixed and pushed. Here's the summary:

## Root Cause

The "Lint Markdown files" step in `gh-pages.yml` ran `markdownlint-cli2 --fix`, committed the fixes, and tried to push. But the remote had already moved (from earlier steps in the SAME workflow or a previous run). The `push_with_retry` function called `git pull --rebase`, which failed because:

1. `markdownlint-cli2 --fix` modified files outside the staged paths (`prompt_md/`, `text_test/`, `README.md` etc.) — these were **unstaged changes**
2. `git pull --rebase` (without `--autostash`) refuses to run with unstaged changes
3. The `|| true` swallowed the error silently, but subsequent retries also failed because the branch was never actually fast-forwarded

## Fix

In all 4 `push_with_retry` functions in `gh-pages.yml`:

```bash
# Before (broken):
git pull --rebase || true

# After (fixed):
git pull --rebase --autostash || { git rebase --abort 2>/dev/null; true; }
```

Two changes:
- **`--autostash`** — stashes any unstaged changes before rebasing, re-applies them after
- **`git rebase --abort`** — if the rebase fails (conflicts), aborts cleanly so the next retry attempt starts from a clean state instead of a half-broken rebase
