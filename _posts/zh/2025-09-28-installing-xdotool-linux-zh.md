---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: 在Linux上安装和使用xdotool
translated: true
type: note
---

要在 Linux 系统上安装 `xdotool`，您可以使用发行版的包管理器。根据您的主机名显示为“XiaoXin”，您可能正在使用 Ubuntu 或基于 Debian 的发行版。以下是常见 Linux 发行版的安装命令：

## Ubuntu/Debian

```bash
sudo apt update
sudo apt install xdotool
```

## CentOS/RHEL/Fedora

```bash
# 新版本系统（dnf）
sudo dnf install xdotool

# 旧版本系统（yum）
sudo yum install xdotool
```

## Arch Linux

```bash
sudo pacman -S xdotool
```

## openSUSE

```bash
sudo zypper install xdotool
```

安装完成后，您可以通过以下命令验证是否安装成功：

```bash
xdotool --version
```

安装完成后，您的 Python 脚本应当能够使用 `xdotool` 获取浏览器标题。该工具常用于自动化 X11 桌面任务，包括获取窗口标题——这正是您的脚本试图实现的功能。

如果安装后仍遇到问题，请确保：

1. 您在 X11 环境（非 Wayland）中运行脚本
2. 您有正在运行的浏览器窗口
3. 浏览器窗口处于焦点状态或可见状态
