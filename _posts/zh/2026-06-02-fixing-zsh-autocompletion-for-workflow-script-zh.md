---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复工作流脚本的Zsh自动补全
translated: true
type: note
---

这是意料之中的——终端使用的是 bash，而非 zsh。你需要在 zsh 中重新加载：`autoload -Uz compinit && compinit`。

以下是我所做的修改：

**`ww/action/action.py`** —— 重写为使用 argparse 并设置默认值：
- 默认工作流程：`gh-pages.yml`
- 默认仓库：`lzwjava/jekyll-ai-blog`（与 `actions check` 保持一致）
- 新增 `--repo` 和 `--ref` 标志
- `ww action`（无参数）→ 在 `lzwjava/jekyll-ai-blog` 上触发 `gh-pages.yml`
- `ww action some-workflow.yml` → 触发该工作流程
- `ww action --ref main` → 在 `main` 分支上触发默认工作流程

**`ww/main.py`** —— 更新帮助文本，将 `<workflow.yml>`（必需）改为显示 `[workflow.yml]`（可选）。

**`~/.zsh/completions/_ww`** —— 新增 `action)` 分支，支持 `--repo`、`--ref` 补全以及 `.yml` 文件通配。
