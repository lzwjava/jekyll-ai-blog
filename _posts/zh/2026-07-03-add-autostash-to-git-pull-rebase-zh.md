---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加自动暂存到git pull rebase
translated: true
type: note
---

已修复并推送。以下是总结：

## 根本原因

`gh-pages.yml` 中的"Lint Markdown files"步骤执行了 `markdownlint-cli2 --fix`，提交了修复内容并尝试推送。但远程仓库已发生变更（源于同一工作流的先前步骤或之前的一次运行）。`push_with_retry` 函数调用了 `git pull --rebase`，但失败的原因为：

1. `markdownlint-cli2 --fix` 修改了暂存路径（`prompt_md/`、`text_test/`、`README.md` 等）之外的文件——这些属于**未暂存的更改**
2. `git pull --rebase`（不带 `--autostash`）在有未暂存更改时拒绝运行
3. `|| true` 静默吞掉了错误，但后续的重试也失败，因为分支实际上从未被快进

## 修复方法

在 `gh-pages.yml` 的全部 4 个 `push_with_retry` 函数中：

```bash
# 之前（有问题的）：
git pull --rebase || true

# 之后（已修复）：
git pull --rebase --autostash || { git rebase --abort 2>/dev/null; true; }
```

两处改动：
- **`--autostash`** — 在变基前暂存所有未暂存的更改，变基后再重新应用
- **`git rebase --abort`** — 如果变基失败（冲突），则干净地终止，以便下一次重试尝试从一个干净的状态开始，而不是处于半破损的变基状态