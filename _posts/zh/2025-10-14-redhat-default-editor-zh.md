---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 红帽企业版Linux默认文本编辑器
translated: true
type: note
---

### Red Hat Enterprise Linux 中的默认文本编辑器

在 Red Hat Enterprise Linux (RHEL) 中，默认文本编辑器是 **Vi**（通常作为 **Vim** 的别名，意为“Vi IMproved”）。Vi 是一款模态命令行文本编辑器，自 1970 年代以来一直是类 Unix 系统的标准配置。它轻量级、普遍适用，并通过 `vim-minimal` 或 `vim-enhanced` 软件包预装在大多数 RHEL 系统上。

#### 为什么选择 Vi/Vim？

- 在图形界面编辑器不实用的服务器环境中表现高效
- 采用基于键盘的操作命令：插入模式用于输入（`i`），命令模式用于编辑（如 `dd` 删除整行，`:wq` 保存并退出）
- 对初学者存在学习曲线，但熟练掌握后功能强大

#### 检查与使用方法

- 运行 `vi 文件名.txt`（或 `vim 文件名.txt`）打开文件
- 查看当前默认编辑器：`echo $EDITOR`（通常输出 `/usr/bin/vi`）
- 若偏好其他编辑器（如先前提到的 Emacs），可在 `~/.bashrc` 中设置 `export EDITOR=emacs`

初学者可通过输入 `vimtutor` 启动交互式教程快速入门。

[Vi 编辑器入门指南 - Red Hat](https://www.redhat.com/en/blog/get-started-vi-editor)
[Linux 技能：9 个教程助你更高效使用文本编辑器 - Red Hat](https://www.redhat.com/en/blog/text-editor-roundup-2022)
