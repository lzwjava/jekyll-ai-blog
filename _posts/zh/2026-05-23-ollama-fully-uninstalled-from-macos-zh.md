---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama 已从 macOS 完全卸载
translated: true
type: note
---

已完成。以下是删除的内容：

- `/Applications/Ollama.app` — 应用程序（登录时自动启动）
- `/Applications/Ollamac.app` — 图形界面客户端
- `/usr/local/bin/ollama` — 命令行工具
- `~/.ollama` — 6.1GB 的模型文件
- `~/Library/Application Support/Ollama` — Electron 应用数据
- `~/Library/LaunchAgents/com.ollama.ollama.plist` — 自动启动守护进程
- 缓存、偏好设置、HTTP 存储 — 所有 Electron 残留文件

释放约 6.1GB 空间。无 Ollama 登录项残留。唯一剩下的是 `~/Library/Containers/` 中一个被 SIP 保护的 Ollamac 容器（约 1KB 元数据），macOS 不允许删除——无害。
