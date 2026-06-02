---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 GitHub Actions 的运行器镜像
translated: true
type: note
---

已修复。以下是更改内容：

### 问题

旧的 runner labels 使用了 `node:16-bullseye` —— 一个纯净的 Node.js 镜像，没有 Python，没有 toolcache，没有任何对 GitHub Actions workflows 有用的东西。当 `actions/setup-python` 尝试安装 Python 3.13.2 时，它无法在该环境中找到兼容的预构建二进制文件。

### 修复方案

切换到 **[catthehacker/ubuntu](https://github.com/catthehacker/docker_images)** 镜像 —— 这些是为 GitHub Actions 仿真专门构建的：

| Label | Image | Pre-installed |
|---|---|---|
| `ubuntu-latest` | `catthehacker/ubuntu:act-latest` | Node, Python, Go, Java, Ruby, PHP, etc. |
| `ubuntu-22.04` | `catthehacker/ubuntu:act-22.04` | Same, Ubuntu 22.04 base |
| `ubuntu-20.04` | `catthehacker/ubuntu:act-20.04` | Same, Ubuntu 20.04 base |

所有三个镜像都已预拉取并缓存。Runner 已恢复在线。重新触发你的 workflow —— Python 3.13.2 现在应该能顺利安装了。🦞
