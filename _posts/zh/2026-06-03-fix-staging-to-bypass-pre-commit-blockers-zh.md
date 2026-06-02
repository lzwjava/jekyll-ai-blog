---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复暂存区以绕过预提交阻止程序
translated: true
type: note
---

已完成。以下是修改的内容及原因：

**根本原因：** `gitmessageai()` 执行了 `git add -A`，这会暂存仓库中所有文件。当 `git commit` 触发 pre-commit 钩子时，会检查所有已暂存的文件——如果任何不相关的文件未通过钩子检查，提交将失败。

**修复——修改了 3 个文件：**

1. `ww/github/gitmessageai.py` —— 新增 `files` 参数。当提供该参数时，仅暂存指定的文件（`git add <file1> <file2>...`），而非执行 `git add -A`。当 `files=None` 时回退到 `git add -A`（保持向后兼容）。

2. `ww/note/note_workflow.py` —— 将 `[created_path]` 传递给 `gitmessageai(files=...)`，确保仅暂存并提交新建的笔记文件。

3. `ww/note/note_queue_process.py` —— 同样修复：`_git_commit_push(files=created_paths)` 将创建的笔记文件列表传递给 `gitmessageai`。

**之前：** `git add -A` → pre-commit 检查仓库所有文件 → 因无关文件失败
**之后：** `git add notes/2026-06-03-foo.md` → pre-commit 仅检查该笔记文件 → 干净提交

所有其他调用 `gitmessageai` 的地方（如 `ww git commit`）仍使用 `files=None` → `git add -A`，因此其他功能行为不变。
