---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Traceroute未默认安装
translated: true
type: note
---

Traceroute 在 Linux 系统上确实可用——这是一个标准的网络诊断工具，用于追踪数据包到达目的地的路径。不过，为了保持基础系统的轻量化，许多现代发行版（如 Ubuntu、Fedora 或 Debian 最小化安装）通常**不会预装该工具**。这就是为什么你在输入 "trac" 时没有看到自动补全提示。

### 快速解决方案
通过包管理器安装即可：
- **Debian/Ubuntu**：`sudo apt update && sudo apt install traceroute`
- **Fedora/RHEL/CentOS**：`sudo dnf install traceroute`（旧版本系统使用 `sudo yum install traceroute`）
- **Arch**：`sudo pacman -S traceroute`

安装完成后，输入 `trac` + Tab 键就能在补全列表中看到 `traceroute` 了。你可以通过运行 `traceroute example.com` 进行测试。

如果你使用的是容器化或极度精简的环境（例如 Alpine Linux），可能需要使用 `tr` 别名或安装其他软件包——如需更具体的解决方案请告知你使用的发行版！
