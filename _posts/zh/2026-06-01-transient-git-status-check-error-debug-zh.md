---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 临时Git状态检查错误调试
translated: true
type: note
---

你说得对——该检查是针对 `.env` 中的 `BASE_PATH` 运行的。

**目录：** `/Users/lzwjava/projects/jekyll-ai-blog`

**代码路径：**

```
note_queue_process.py:process_queue()
  → _check_uncommitted()
    → check_uncommitted_changes()  (note_workflow.py:25)
      → _git_toplevel()
        → get_base_path()  →  读取 BASE_PATH 环境变量
        → git -C /Users/lzwjava/projects/jekyll-ai-blog rev-parse --show-toplevel
      → git -C <toplevel> status --porcelain
```

目前该仓库是干净的：

```
$ git -C /Users/lzwjava/projects/jekyll-ai-blog status --porcelain
(空)
```

所以错误是暂时的——当观察者第二次运行 `process_queue()` 时，博客仓库在那时处于脏状态（很可能是第一次 `process_queue` 调用中的 `_git_pull_rebase()` 或之前的 `gitmessageai` 提交留下了某些暂存/脏的内容）。

关键问题：第一次 `process_queue()` 运行时没有发现未提交的更改，创建了一个笔记（因重复而失败），没有提交（没有 `created_paths`），但它确实调用了 `_git_pull_rebase()`。如果那次 rebase 遇到冲突或留下 `.git/REBASE_HEAD` 或类似状态，第二次运行时的 `check_uncommitted_changes()` 就会看到它。

如果这种情况持续发生，你可以在检查之前添加调试输出，看看 `git status --porcelain` 实际报告了什么：

```python
# 在 check_uncommitted_changes() 中，第 34 行之后：
if result.stdout.strip():
    print(f"[debug] git status output: {result.stdout!r}")  # 添加此行
```