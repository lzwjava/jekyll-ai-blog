---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理远程分支的修剪操作
translated: true
type: note
---

`git fetch --prune` 是一种保持本地远程分支引用整洁和最新的方法。

### 功能说明

* **`git fetch`** 通常会在不触及本地分支的情况下，更新您对远程分支的本地副本（例如 `origin/main`、`origin/feature-x`）。
* 随着时间的推移，远程仓库可能会删除或重命名某些分支。如果不进行清理，您的本地仓库仍会显示那些陈旧的远程跟踪分支（例如 `origin/feature-old`）。
* **添加 `--prune`** 参数会告知 Git：*“如果远程不再拥有某个分支，则删除我本地对应的远程跟踪引用。”*

因此，运行 `git fetch --prune` 后，您本地的远程分支列表将与远程当前的状态完全一致。

### 示例演示

1. 远程拥有分支：`main`、`feature-a`
2. 您运行 `git fetch` → 本地生成 `origin/main`、`origin/feature-a`
3. 有人在远程删除了 `feature-a`
4. 若运行 `git fetch`，本地仍会显示 `origin/feature-a`（陈旧引用）
5. 若运行 `git fetch --prune`，Git 将检测到 `feature-a` 已消失，并从本地仓库移除 `origin/feature-a`

### 实用价值

* 保持 `git branch -r`（远程分支列表）整洁
* 避免切换到或合并到上游已不存在的分支时产生混淆
* 常与别名配合使用（如 `git fetch -p`），或通过以下配置设为默认行为：

  ```bash
  git config fetch.prune true
  ```

这样每次执行 `git fetch` 时都会自动清理陈旧分支。

---

需要进一步了解 **修剪操作与标签的关联机制** 吗？（默认情况下 `git fetch --prune` 仅处理分支，而标签的处理方式有所不同）
