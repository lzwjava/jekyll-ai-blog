---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub 预提交钩子指南
translated: true
type: note
---

**问题：** 如何使用带有 `.pre-commit-config.yaml` 文件的 pre-commit hooks，以及当仓库托管在 GitHub 上时，它们是否有效？

---

**回答：**

## 概述

`pre-commit` 框架的 pre-commit hooks 本质上是 **client-side** 的——它们在每个开发者的本地机器上运行。但是，您可以使用两个互补的层：

1. **Local hooks** —— 在每个开发者的机器上，在每次 `git commit` 之前运行
2. **Server-side / CI enforcement** —— 通过 GitHub Actions 或 pre-commit.ci 在 GitHub 上运行

---

## 第一部分：本地设置（每个团队成员都必须执行此操作）

### 步骤 1 — 安装 `pre-commit` 工具

```bash
pip install pre-commit
```

### 步骤 2 — 将 `.pre-commit-config.yaml` 提交到您的仓库

此文件（您展示的文件）应位于仓库根目录，并像其他文件一样提交。它需要为每个 hook 来源指定一个 `rev`（版本标签）：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0   # <-- specify a version tag!
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: https://github.com/psf/black
    rev: 23.12.0  # <-- specify a version tag!
    hooks:
      - id: black
```

### 步骤 3 — 将 hooks 安装到本地 git 仓库

```bash
pre-commit install
```

这会将 hook 脚本安装到您的 `.git/hooks` 目录中，因此 `pre-commit` 现在会在每次 `git commit` 时自动运行。

### 步骤 4 — （可选）手动运行所有文件

```bash
pre-commit run --all-files
```

---

## 第二部分：提交时会发生什么

pre-commit hook 在您输入提交消息之前首先运行。如果它以非零退出，提交将被中止。您会看到类似以下输出：

```
Trim Trailing Whitespace.......................Passed
Fix End of Files...............................Passed
black..........................................Failed
- hook id: black
- files were modified by this hook
```

当 hooks **auto-fix** 文件（例如 Black 重新格式化代码）时，被修改的文件将作为未暂存更改保留。您必须暂存它们并再次提交：

```bash
git add .
git commit -m "your message"
```

您始终需要暂存并提交 hooks 所做的任何更改——这让您对进入代码库的内容有最终决定权。

要**临时绕过 hooks**（请谨慎使用）：

```bash
git commit -m "WIP" --no-verify
```

---

## 第三部分：它与 GitHub 托管的仓库兼容吗？

### 关键限制

pre-commit hooks 是 client-side 的——它们由本地操作（如提交和合并）触发，而不是服务器端网络操作。这意味着：

- GitHub **不会**自动运行它们
- 如果团队成员没有运行 `pre-commit install`，他们的提交将完全绕过 hooks
- 通过 **GitHub web UI** 进行的提交完全跳过本地 hooks

### 解决方案 A：GitHub Actions（推荐用于团队）

某人可能通过 GitHub UI 创建拉取请求，在这种情况下 pre-commit hooks 不会原生运行。要在每次 push/PR 上强制执行 hooks，请添加一个工作流文件：

```yaml
# .github/workflows/pre-commit.yml
name: pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
      - uses: pre-commit/action@v3.0.1
```

默认情况下，此 action 会针对所有文件运行所有 hooks。您也可以通过 `extra_args` 指定单个 hook。

### 解决方案 B：pre-commit.ci（最简单选项）

您可以在本地和云端运行 hooks。作为使用 `https://pre-commit.ci` 的 CI 检查，您可以强制拉取请求通过 hooks，并自动修复如样式等 trivial 问题，即使提交者没有本地安装。

只需在 [pre-commit.ci](https://pre-commit.ci) 登录，连接您的 GitHub 仓库，它就会处理一切——无需额外的 workflow 文件。

---

## 总结表格

| 层 | 谁运行它 | 强制执行格式化 | 每个开发者需要设置 |
|---|---|---|---|
| Local `pre-commit install` | 开发者的机器 | 是，阻塞提交 | 是 |
| GitHub Actions | GitHub CI runner | 是，失败 PR/push | 否（自动） |
| pre-commit.ci | 云服务 | 是，可自动修复 | 否（自动） |

团队的推荐方法是**两者兼用**：本地 hooks 用于快速反馈，加上 GitHub Actions 或 pre-commit.ci 作为安全网。

---

**参考资料：**

- [pre-commit 官方文档](https://pre-commit.com/)
- [pre-commit/action on GitHub Marketplace](https://github.com/marketplace/actions/pre-commit)
- [Stefanie Molin – How to Set Up Pre-Commit Hooks](https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/)
- [Running pre-commit hooks as GitHub Actions](https://thomasthornton.cloud/2022/08/04/running-pre-commit-hooks-as-github-actions/)
- [pre-commit.ci](https://pre-commit.ci)
