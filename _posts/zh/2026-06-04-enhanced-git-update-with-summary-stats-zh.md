---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 增强版Git更新与摘要统计
translated: true
type: note
---

已完成。以下是添加到 `ww/git/git_update.py` 中的内容：

1. **`_get_short_stats(repo_path, old_head, new_head)`** — 在两个提交之间运行 `git rev-list --count` 和 `git diff --shortstat`，返回 `(commits, files, ins, dels)`

2. **`pull_repo()`** 现在在拉取前记录 HEAD，拉取后检查 HEAD，并返回 `(repo_path, success, stats)` 而不是单纯的 `bool`

3. **输出末尾的摘要表** — 仅当存在实际有新提交的仓库时才打印。按字母顺序排序，并包含 TOTAL 行。

有更新时的输出格式：

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

当所有仓库都已是最新（无需拉取）时，不打印表格 — 仅显示摘要行。
