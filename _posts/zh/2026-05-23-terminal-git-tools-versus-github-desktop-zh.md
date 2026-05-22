---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端Git工具对比GitHub Desktop
translated: true
type: note
---

**问题：** GitHub Desktop 中的文件查看器很棒，对吧？查看文件时可以直接导航到文件？

**答案：**

GitHub Desktop 的文件查看器还算不错，但老实说，相比你可能期望的，它相当有限。以下是实际情况：

**GitHub Desktop 的优势：**
- 变更文件的并排或统一差异视图
- 点击变更文件列表中的文件 → 跳转到其差异视图
- 差异视图支持语法高亮

**不足之处：**
- 你只能看到 *差异*，而不是完整文件的上下文
- 不支持跨文件搜索
- 没有完整仓库的树形导航
- 大变更集时响应缓慢

**更适合你的工作流程的替代方案（终端优先）：**

```bash
# 查看所有变更的文件
git status

# 查看特定文件的差异
git diff path/to/file.py

# 直接在编辑器中打开变更文件
git diff --name-only | xargs code  # VSCode
git diff --name-only | xargs nvim  # neovim

# 交互式差异浏览器（最佳 CLI 选项）
git diff | delta        # https://github.com/dandavison/delta
git diff | tig         # ncurses git 浏览器
```

**`delta`** 是最大的升级——它在终端中为你提供语法高亮、并排的差异视图，行号，甚至文件链接。安装：

```bash
brew install git-delta
```

```ini
# ~/.gitconfig
[core]
    pager = delta
[delta]
    side-by-side = true
    navigate = true
    line-numbers = true
```

**`tig`** 提供了一个完整的 ncurses TUI，用于浏览提交、差异、文件树——功能接近 GitHub Desktop，但运行在终端中。

鉴于你在 M2 上以终端为先，`delta` + `tig` 每次都会击败 GitHub Desktop 的文件视图。GitHub Desktop 主要对避免使用终端的人有用——这不适合你。