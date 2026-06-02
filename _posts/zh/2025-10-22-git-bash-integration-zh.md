---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 将 Git Bash 集成到 Windows 终端
translated: true
type: note
---

是的，Git Bash 可以在控制台窗口中运行（默认使用其自带的 MinTTY 终端），并能与 Windows Terminal 无缝集成。您只需在 Windows Terminal 设置中为其添加自定义配置文件——指向 Git 安装目录中的 `bash.exe` 可执行文件（通常位于 `C:\Program Files\Git\bin\bash.exe`）。添加后，您就可以像使用其他 shell 一样在新标签页或窗格中启动它。

您对 Windows Terminal 的功能限制存在误解：它支持的远不止 PowerShell 和命令提示符。开箱即用即可支持这两者，外加 WSL 发行版、Azure Cloud Shell，甚至包括 Git Bash 或 Cygwin 等自定义 shell。它被设计成能灵活承载几乎所有命令行环境。

[将 Git-Bash 添加到新版 Windows Terminal](https://stackoverflow.com/questions/56839307/adding-git-bash-to-the-new-windows-terminal)
[将 Git-Bash 添加到 Windows Terminal](https://www.timschaeps.be/post/adding-git-bash-to-windows-terminal/)
[在 Windows Terminal 中，如何将 bash 添加为 shell 选项之一？](https://superuser.com/questions/1763652/in-windows-terminal-how-do-i-add-bash-as-one-of-the-shell-options)
