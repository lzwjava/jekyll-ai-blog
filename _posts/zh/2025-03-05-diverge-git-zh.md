---
audio: false
generated: true
lang: zh
layout: post
title: Git分支分叉
translated: true
type: note
---

当你的本地 `main` 分支与远程 `origin/main` 分支在 Git 中出现分叉（分别拥有 74 个和 70 个不同提交）时，说明它们拥有共同祖先，但之后各自产生了独立提交。你的目标是通过将本地分支重置到共同祖先（即"两者的父提交"），然后使用 `git pull` 获取远程变更，使本地 `main` 分支与 `origin/main` 保持一致。这将有效丢弃你的本地分叉提交，采用远程提交。以下是实现此目标的步骤。

### 修复分叉的步骤

1. **获取最新远程变更**
   首先确保本地仓库拥有来自远程的最新信息。这会更新你对 `origin/main` 的引用，但尚未更改本地 `main` 分支。

   ```bash
   git fetch origin
   ```

2. **查找共同祖先提交**
   使用 `git merge-base` 识别本地 `main` 与 `origin/main` 的共同祖先提交。这是分支分叉的起点。

   ```bash
   ancestor=$(git merge-base main origin/main)
   ```

   该命令将共同祖先的提交哈希值存入变量 `ancestor`。

3. **将本地 `main` 重置至共同祖先**
   将本地 `main` 分支重置到共同祖先提交。`--hard` 选项会同时更新分支指针和工作目录，丢弃此时间点之后的所有本地提交和变更。

   ```bash
   git reset --hard $ancestor
   ```

   **注意**：此操作将丢弃工作目录和暂存区中所有未提交的变更，以及本地 `main` 分支独有的 74 个提交。如需保留这些内容，请先创建备份分支（参见下文"可选备份"）。

4. **拉取远程变更**
   现在从 `origin/main` 拉取变更。由于本地 `main` 已处于共同祖先，而 `origin/main` 领先 70 个提交，这将快速前进你的本地 `main` 分支以匹配 `origin/main`。

   ```bash
   git pull origin main
   ```

   完成后，你的本地 `main` 分支将与 `origin/main` 完全一致，所有本地分叉提交均被丢弃。

### 完整命令序列

以下是需要执行的完整命令序列：

```bash
git fetch origin
ancestor=$(git merge-base main origin/main)
git reset --hard $ancestor
git pull origin main
```

### 会发生什么？

- **步骤 1 之后**：本地仓库知晓 `origin/main` 的最新状态
- **步骤 2 之后**：已识别共同祖先提交（例如类似 `abc123` 的哈希值）
- **步骤 3 之后**：本地 `main` 重置至 `abc123`，丢失 74 个独有本地提交
- **步骤 4 之后**：`git pull` 将 `main` 快速前进至 `origin/main`，纳入远程分支的 70 个提交

最终你的本地 `main` 会与 `origin/main` 完全一致，实现采用远程分支的目标。

### 可选备份

如果不确定是否要丢弃本地提交，可在重置前创建备份分支进行保留：

```bash
git branch backup-main
```

在执行 `git reset` 命令前运行此命令。你的 74 个本地提交将保留在 `backup-main` 分支中，后续可按需查看。

### 重要说明

- **未提交的变更**：如需保留工作目录或暂存区中的未提交变更，请在重置前贮藏它们：

  ```bash
  git stash
  ```

  流程完成后，可通过 `git stash pop` 恢复变更。
- **原理说明**：通过重置到共同祖先再拉取，可确保干净地快速前进至 `origin/main`，避免直接拉取分叉分支可能产生的合并冲突。

遵循这些步骤，你将成功重置本地 `main` 分支以匹配目标状态。
