---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Git Fetch与Prune操作详解
translated: true
type: note
---

### 什么是 `git fetch`？
`git fetch` 会从远程仓库下载最新变更（提交、分支、标签），但不会将这些变更合并到当前分支。它会更新本地的远程追踪分支（例如 `origin/main`）以匹配远程仓库的状态。这能使本地仓库保持同步，但不会改动你的工作文件或本地分支。

### `--prune` 选项的作用是什么？
`--prune` 标志会指示 Git 删除远程已不存在但本地仍保留的远程追踪分支。例如，若有人在 GitHub 上删除了某个分支，你本地的对应分支（如 `origin/old-branch`）仍会保留，除非执行清理操作。

### `git fetch --prune` 如何工作？
- **执行方式**：通过 `git fetch --prune`（或简写 `git fetch -p`）运行。该命令将获取与清理操作合并为一步。
- **执行步骤**：
  1. Git 连接远程仓库并获取更新，同步远程追踪分支以反映新的提交、新增分支或已删除分支。
  2. 扫描本地过时的远程追踪分支（即远程仓库已不存在的分支）并在本地删除它们。
- **效果**：本地仓库保持最新且整洁。此操作不会执行合并——属于只读式同步。

### 实际示例
假设你的仓库存在：
- 本地分支：`main`，追踪 `origin/main`
- 过时的本地远程追踪分支：`origin/deleted-feature`

对 `origin` 执行 `git fetch --prune` 后：
- 获取所有新提交
- 删除本地的 `origin/deleted-feature`（因为远程分支已不存在）
- 不会影响你的本地分支

### 核心意义
该操作意为“获取最新远程数据并清理本地过时的引用”。建议定期使用此命令，避免因旧分支引用导致混淆。其效果等同于先执行 `git fetch` 再执行 `git remote prune origin`，但以更便捷的方式合并。为保障安全，该操作仅影响远程追踪分支，不会触及你的本地工作内容。
