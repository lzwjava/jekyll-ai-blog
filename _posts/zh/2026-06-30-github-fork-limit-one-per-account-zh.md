---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub 复刻限制：每个账户一个
translated: true
type: note
---

问题：我可以在同一个 GitHub 账号下，将同一个仓库分叉两次，并命名为不同的名称吗？

答案：

不可以——GitHub 每个账号/组织**只允许对给定仓库进行一次分叉**。分叉关系基于上游仓库，而非名称。一旦你分叉了 `owner/repo`，再次点击“Fork”只会重定向到你已有的分叉。

要获得第二个不同名称的副本，有以下变通方法：

**1. 重命名现有分叉，然后再次分叉（仍然只能有一个真正的分叉）**——重命名并不会释放第二个分叉名额。跳过此方法，它行不通。

**2. 裸克隆 + 推送到新仓库（最常见，无分叉关系）：**

```bash
# 先创建新的空仓库（通过 gh CLI）
gh repo create lzwjava/repo-copy --private

# 镜像源仓库
git clone --bare https://github.com/owner/repo.git
cd repo.git
git push --mirror https://github.com/lzwjava/repo-copy.git
cd .. && rm -rf repo.git
```

这样你会得到一个独立的仓库（包含所有分支/标签），名称可任意指定，但**不会**显示为分叉（没有“forked from”链接，默认也没有向上游仓库提交 PR 的界面）。你可以手动添加上游仓库：

```bash
git clone https://github.com/lzwjava/repo-copy.git
cd repo-copy
git remote add upstream https://github.com/owner/repo.git
git fetch upstream
```

**3. 使用第二个账号/组织**——在个人账号下分叉原始仓库，再在你拥有的组织下分叉一次。每个命名空间只能有一个分叉。

**4. `gh repo fork` 配合 `--fork-name`（仍然只有一个分叉）：**

```bash
gh repo fork owner/repo --fork-name my-custom-name --clone
```

这允许你为单个分叉命名，但无法通过此方式创建*第二个*分叉。

对于你的工作流程（CLI 代理、实验），选项 2 是最干净的——你可以自由修改独立仓库，不受分叉限制，并在需要同步时手动配置 `upstream`。