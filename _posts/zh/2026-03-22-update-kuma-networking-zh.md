---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新 Uptime Kuma 容器网络
translated: true
type: note
---

Uptime Kuma 已经在 `librechat_default` 上了。让我也将它连接到其他网络：

现在让我验证对它们的连接性：所有都已连接并可达：

| Service | Container Name | Port | Status |
|---|---|
| LibreChat | `LibreChat` | 3080 | ✅ 200 |
| Gitea | `gitea` | 3000 | ✅ 200 |
| SearXNG | `searxng` | 80 | ✅ 20 |
| Nextcloud | `nextcloud-app-1` | 80 | ✅ reachable (400 = responding, just needs proper request) |

现在进入 Uptime Kuma 并更新你的 monitor URLs，使用容器名称而不是 IP 地址。例如：
- `http://LibreChat:3080/`
- `http://gitea:300/`
- `http://searxng:8080/`
- `http://nextcloud-app-1:80/`

⚠️ 同样的 caveat — 这些连接会在容器重启后消失。要我在 compose 文件中使其永久化吗？
