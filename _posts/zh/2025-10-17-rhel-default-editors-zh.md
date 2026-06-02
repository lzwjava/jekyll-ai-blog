---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: RHEL极简版默认文本编辑器
translated: true
type: note
---

在 Red Hat Enterprise Linux (RHEL) 系统中，特别是最小化安装（服务器和轻量级环境的默认选项）时，系统默认仅预装由 `vim-minimal` 软件包提供的 **vi** 文本编辑器。这为您在终端中编辑文件提供了基础且兼容经典 `vi` 命令的实现方案。

- **完整版 `vim`**（具备更多增强功能如语法高亮等）不会默认安装。您可通过 `sudo dnf install vim-enhanced` 命令添加
- **Nano** 和 **Emacs** 不包含在最小化安装中。它们虽存在于软件仓库，但需要显式安装：
  - 安装 Nano：`sudo dnf install nano`
  - 安装 Emacs：`sudo dnf install emacs`

这种设计使得最小化安装保持轻量（总计约200-300个软件包），以优先保障安全性和性能。若执行完整版桌面或服务器安装（非最小化），根据所选环境可能会预装更多工具。

[Nano 入门指南（Red Hat）](https://www.redhat.com/en/blog/getting-started-nano)
[为何 RHEL 默认安装两个 vim 版本？](https://unix.stackexchange.com/questions/699071/why-rhel-has-two-vim-installed-by-default)
[RHEL 9 软件包清单](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/package_manifest/index)
