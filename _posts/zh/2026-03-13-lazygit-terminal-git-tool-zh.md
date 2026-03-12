---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Lazygit 简单终端 Git 利器
translated: true
type: note
---

我会为你搜索关于 Lazygit 的全面信息。现在让我搜索更多关于安装和功能的特定信息。---

**问题：** 什么是 Lazygit 的全面介绍，这是一个 CLI 工具？

**回答：**

## 概述

Lazygit 是一个简单的 git 命令终端 UI，使用 Go 语言和 gocui 库编写，让你在终端中心环境中感受到 Sourcetree 的感觉。它是一个轻量级的、基于 CLI 的 Git UI，让开发者在使用 UI 的同时，速度与在终端中使用 CLI 命令一样快。

## 历史和目的

Lazygit 由澳大利亚开发者 Jesse Duffield 于 2018 年创建，作为一个旨在减少记住和输入长 Git 命令摩擦的副项目，并在 GitHub 上开源，迅速在开发者中获得关注。

## Lazygit 创建的原因

创建者的动机源于对 Git 复杂性的沮丧：交互式 rebase 需要在编辑器中编辑 TODO 文件，分级暂存文件部分需要逐个 hunk 步骤，简单操作往往需要复杂的命令序列。

## 技术基础

该工具完全使用 Go 语言编写，这使其快速、可移植且易于安装为单个二进制文件，无需依赖，并且 Go 二进制文件启动时间仅需毫秒级，即时启动。

## 主要功能

### 视觉界面和组织

Lazygit 的 UI 分为六个面板或部分，还有一个预览面板，让你预览未暂存更改、提交、日志、文件内容等。你可以使用箭头键或 vim 风格的 H/J/K/L 导航在 TUI 面板间导航，有些面板有多个标签页。

### 键盘驱动的工作流

最绝妙的功能是它完全由键盘驱动——你永远不需要触摸鼠标来使用 lazygit。你唯一需要记住的键盘快捷键是 ?，它会根据活动面板显示上下文相关的可用操作。

### 核心操作

**暂存和提交：**
要以闪电般的速度暂存文件，使用箭头键在文件间导航，按空格键在暂存和未暂存状态间切换文件。

**交互式 Rebasing：**
你可以按 i 开始交互式 rebase，然后在继续 rebase 前，对 TODO 提交进行 squash (s)、fixup (f)、drop (d)、edit (e)、上移 (ctrl+k) 或下移 (ctrl+j)。在 Lazygit 中，所有交互式 rebase 的简单用例都支持各自的键绑定，你实际上是通过 Lazygit 编辑那个 TODO 文件，但一切只需单次按键。

**Cherry-Picking：**
你可以在提交上按 shift+c 复制它，然后按 shift+v 粘贴（cherry-pick）它。

**分支管理：**
要创建新分支，按 n；要删除分支，按 d，然后指定是要删除本地还是远程仓库的分支。

**合并冲突解决：**
要解决合并冲突，先按 M 合并分支，然后选择合并类型并按 Enter；如果发生任何合并冲突，冲突文件会出现在文件面板中，你可以选择正确的合并冲突并按空格键解决。

### 高级功能

Lazygit 支持从旧提交创建自定义 patch，允许你从提交中移除 patch、分拆新提交、反向应用 patch 到 index 等。你可以创建 worktrees 来同时处理多个分支，而无需在切换时进行 stashing 或创建 WIP 提交。你可以在提交视图中按 b 将提交标记为 good/bad 以开始 git bisect。

## 跨平台支持

Lazygit 可以在 Linux、macOS、FreeBSD 和 Windows 上运行。

## 安装

Lazygit 提供多种安装方法：

**macOS：**
你可以使用 brew 在 macOS 上轻松安装 lazygit：brew tap jesseduffield/lazygit && brew install lazygit。

**Windows：**
你可以使用 Windows Terminal 中的 winget 命令安装 lazygit。

**Linux：**
Ubuntu 的 Lazygit 包通过 Launchpad PPA 提供：sudo add-apt-repository ppa:lazygit-team/daily && sudo apt update && sudo apt install lazygit。

**从源代码：**
如果你安装了 Go，可以使用：go get github.com/jesseduffield/lazygit，然后在 git 仓库的终端中调用 lazygit。

## 配置

Lazygit 是 config-as-code：单个 YAML 文件位于 ~/.config/lazygit/config.yml，你可以覆盖键绑定、添加自定义 pull-request 命令，或将输出管道到首选 pager。

## 目标受众

Lazygit 非常适合初学者，它提供视觉界面，使 Git 操作更直观，而无需记忆复杂的命令行语法。然而，如果你生活在 IDE 中，其 Git 面板已经提供大多数这些功能，或者你进行大量脚本自动化，其中原始 CLI 更快，你可能不需要 lazygit。

## 入门

只需在 git 仓库的终端中输入 `lazygit` 即可启动工具。如果你愿意，还可以添加别名：echo "alias lg='lazygit'" >> ~/.zshrc。

---

## 参考资料

- [GitHub - jesseduffield/lazygit: simple terminal UI for git commands](https://github.com/jesseduffield/lazygit)
- [How to Use Lazygit to Skyrocket Your Git Efficiency](https://chishengliu.com/posts/lazygit-tutorial/)
- [How to Use Lazygit to Improve Your Git Workflow](https://www.freecodecamp.org/news/how-to-use-lazygit-to-improve-your-git-workflow/)
- [Level-up Git with lazygit](https://medium.com/@rasmusfangel/level-up-git-with-lazygit-b5e6c923c5d7)
- [What is LazyGit?](https://graphite.com/guides/lazygit)
- [lazygit Keybindings](https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md)
- [Install and Use lazygit](https://computingforgeeks.com/how-to-install-and-use-lazygit-a-simple-terminal-ui-for-git-commands/)
- [Make advanced Git tasks simple with Lazygit](https://opensource.com/article/20/3/lazygit)
- [Lazygit, the convenience of GUI with the power of git CLI](https://pawelgrzybek.com/lazygit-the-convenience-of-gui-with-the-power-of-git-cli/)
- [The (lazy) Git UI You Didn't Know You Need](https://www.bwplotka.dev/2025/lazygit/)
- [Lazygit: A Simple Terminal UI That Makes Git Human-Friendly](https://www.blog.brightcoding.dev/2025/08/14/lazygit-a-simple-terminal-ui-that-makes-git-human-friendly/)
- [Lazygit: The terminal UI that makes git actually usable](https://www.bytesizego.com/blog/lazygit-the-terminal-ui-that-makes-git-actually-usable)