---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 私密笔记实现摘要
translated: true
type: note
---

所有更改均正常工作。以下是已实现内容的摘要：

## 变更摘要

### 1. `ww/note/note_queue.py` — `enqueue_clipboard()` 接受 `private` 参数

- 添加了 `private=False` 参数
- 当为 `True` 时，在队列条目的额外字典中存储 `{"private": True}`

### 2. `ww/note/note_queue_process.py` — 私有笔记处理

- 添加了 `PRIVATE_NOTES_DIR = "/Users/lzwjava/projects/jekyll-ai-blog/private-note"`
- 处理带有 `"private": True` 的队列条目时，在 `PRIVATE_NOTES_DIR` 中创建笔记（通过 `create_note_from_content(content, directory=...)`）
- 私有笔记**排除**在 `created_paths` 之外，因此不会被 git 提交/推送
- 所有其他处理（MathJax 修复、表格修复）保持不变

### 3. `ww/note/note_workflow.py` — `--sync` 路径支持 `--private`

- 添加了 `PRIVATE_NOTES_DIR` 常量
- 为 argparse 添加了 `--private`
- 当设置了 `--private` 时，跳过 `check_uncommitted_changes()`、`git_pull_rebase()` 以及 git 提交/推送——仅在私有目录中创建笔记

### 4. `ww/main.py` — 路由 `--private` 标志

- **快速路径**（`ww note --private`）：检测 `sys.argv` 中的 `--private`，移除它，将 `private=True` 传递给 `enqueue_clipboard()`
- **同步路径**（`ww note --private --sync`）：将 `--private` 保留在 `sys.argv` 中，由 `note_workflow.py` 的 argparse 处理
- 添加了帮助文本：`ww note --private`

### 5. `~/.zsh/completions/_ww` — Tab 补全

- 在 `note)` 参数完成中，添加了 `'--private[保存到私有笔记目录，跳过 git push]'`
