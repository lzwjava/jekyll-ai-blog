---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Git Cherry-Pick 功能概述与使用指南
translated: true
type: note
---

### 什么是 Git Cherry-Pick？

Git cherry-pick 是一个允许你将特定提交（或一组提交）的更改应用到当前分支的命令，它会创建一个包含这些更改的新提交。当你希望从某个分支选取特定修复或功能而不合并整个分支时，这个命令非常有用。与合并（会整合所有历史记录）不同，cherry-pick 会选择性地复制更改。

### Git Cherry-Pick 的内部工作原理

1. **选择提交**：你指定一个包含所需更改的提交哈希（例如，通过 `git log` 查找）。

2. **应用更改**：Git 从该提交中获取差异（实际的代码更改），并尝试将其应用到当前分支的工作目录，尽可能使用 Git 的三路合并逻辑。

3. **创建新提交**：如果成功，将在你的分支上创建一个新提交，其中包含：
   - 与原始提交相同的更改。
   - 一个新的提交哈希（因为这是一个全新的提交）。
   - 一条引用原始提交的提交消息（例如，通过 `-x` 标志附加“cherry picked from commit <hash>”）。

   如果存在合并冲突（例如，目标分支有不兼容的更改），Git 会暂停并让你在提交前手动解决冲突。

该过程不会改变原始提交的历史记录——它只是复制更改。这使得 cherry-pick 非常适合向后移植错误修复或选择性应用功能。

### 基本使用步骤

1. 确保你位于目标分支上（使用 `git checkout <branch>` 切换分支）。
2. 找到你需要的提交哈希（例如，`git log --oneline`）。
3. 运行：`git cherry-pick <commit-hash>`
   - 对于多个提交：`git cherry-pick <hash1> <hash2>`
   - 使用选项如 `-n`（不提交，用于暂存）或 `-x`（引用原始提交）。
4. 如果出现冲突，编辑文件，使用 `git add` 暂存，然后运行 `git cherry-pick --continue`。
5. 如果中途中止：`git cherry-pick --abort`。

### 示例场景

假设你有一个功能分支，提交记录为 A -> B -> C，你希望将提交 B cherry-pick 到主分支上。

- 在主分支上：`git checkout main`
- `git cherry-pick B`（将 B 替换为实际哈希）

这会将 B 的更改作为新提交 D 添加到主分支，而不会引入 A 或 C。原始的 B 仍保留在功能分支中。

### 注意事项与技巧

- 避免 cherry-pick 合并提交（具有多个父提交的提交），因为这可能导致问题——使用 `git cherry-pick -m 1 <merge-commit>` 指定父提交。
- 它不会保留提交的元数据（如作者日期），但 `git cherry-pick --edit` 允许你修改提交消息。
- 对于有顺序的更改，按顺序 cherry-pick 多个提交以避免遗漏依赖项。
- cherry-pick 后务必进行测试，因为如果上下文不同，可能会引入错误。

更多详细信息，请参阅官方 Git 文档：https://git-scm.com/docs/git-cherry-pick。如果你遇到具体问题，请分享你的 Git 日志输出！
