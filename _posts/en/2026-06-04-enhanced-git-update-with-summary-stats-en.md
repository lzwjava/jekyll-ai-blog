---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhanced Git Update with Summary Stats
translated: false
type: note
---

Done. Here's what I added to `ww/git/git_update.py`:

1. **`_get_short_stats(repo_path, old_head, new_head)`** — runs `git rev-list --count` and `git diff --shortstat` between two commits, returns `(commits, files, ins, dels)`

2. **`pull_repo()`** now records HEAD before pulling, checks HEAD after, and returns `(repo_path, success, stats)` instead of just `bool`

3. **Summary table** at the end of the output — only prints when there are repos with actual new commits. Sorted alphabetically, with a TOTAL row.

Output format when there are updates:

```
Done: 29 current, 58 updated, 0 failed (39.0s)

Repo         commits  files changed  insertions(+)  deletions(-)
───────────  ───────  ─────────────  ─────────────  ───────────
ClickHouse         3             19           1140          137
DeepSeek-V3        1              2             45           12
llama.cpp          5              8            320           95
nanochat           2              4            180           30
───────────  ───────  ─────────────  ─────────────  ───────────
TOTAL             11             33           1685          274
```

When all repos are already current (no pulls needed), no table is printed — just the summary line.
