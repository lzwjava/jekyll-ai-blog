---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama已从系统中完全移除
translated: true
type: note
---

全面总结 — **Ollama 已完全从启动项中移除，且未在任何位置运行**：

| 检查项 | 结果 |
|--------|------|
| **launchd（用户代理）** `com.ollama.ollama` | ❌ 未注册 |
| **LaunchAgent plist（用户）** | ❌ 未找到 plist 文件 |
| **LaunchAgent plist（系统）** | ❌ 未找到 plist 文件 |
| **LaunchDaemon plist（系统）** | ❌ 未找到 plist 文件 |
| **brew services** | ❌ 未加载，未运行 |
| **ollama 进程运行中** | ❌ 零个进程 |
| **macOS 登录项** | ❌ 未列出 |
| **OLLAMA_ 环境变量** | ❌ 未设置 |
| **11434 端口监听** | ❌ 默认 Ollama 端口无监听 |
| **Docker Ollama 容器** | ❌ 未运行 |

全部九个自动启动攻击面均已被清理。系统启动时不会启动 Ollama，当前也无任何服务在运行或监听。