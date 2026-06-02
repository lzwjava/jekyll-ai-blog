---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器端口安全审计摘要
translated: true
type: note
---

以下是详细分解，老板：

| Port | Service | Listening | Exposed To |
|------|---------|-----------|------------|
| **22** | sshd | ✅ | Anywhere |
| **80** | nginx | ✅ | Anywhere |
| **3001** | docker-proxy | ✅ | Anywhere |
| **5000** | — | ❌ not listening | Anywhere (rule exists) |
| **7890** | mihomo (proxy) | ✅ | Anywhere (docker0) |
| **8080** | docker-proxy | ✅ | Anywhere |
| **11434** | ollama | ✅ | localhost only |
| **18789** | openclaw-gateway | ✅ | localhost + 192.168.1.0/24 |

**观察：**

- **Port 5000/tcp** 有 ufw 规则，但实际上没有在监听 — 可能是停止的 Nextcloud 容器留下的？
- **Port 3001** 和 **8080** 通过 Docker 完全暴露在互联网上。这些很可能分别映射到 LibreChat 和 Nextcloud。
- **docker0 上的 7890** 是 SearXNG 的 mihomo proxy — 已标记为允许，但你的 SearXNG 显示 0% uptime，所以那里有些问题。
- **Ollama (11434)** 正确限制为仅 localhost。
- **OpenClaw (18789)** 很好地限制为仅 LAN。

要我深入调查 SearXNG 问题，还是收紧这些规则中的任何一个？
