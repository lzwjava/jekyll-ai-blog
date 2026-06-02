---
audio: false
generated: true
image: false
lang: en
layout: post
title: Update Uptime Kuma Container Networking
translated: false
type: note
---

Uptime Kuma is already on `librechat_default`. Let me connect it to the other networks too:Now let me verify connectivity to all of them:All connected and reachable:

| Service | Container Name | Port | Status |
|---|---|
| LibreChat | `LibreChat` | 3080 | ✅ 200 |
| Gitea | `gitea` | 3000 | ✅ 200 |
| SearXNG | `searxng` | 80 | ✅ 20 |
| Nextcloud | `nextcloud-app-1` | 80 | ✅ reachable (400 = responding, just needs proper request) |

Now go into Uptime Kuma and update your monitor URLs to use the container names instead of IP addresses. Like:
- `http://LibreChat:3080/`
- `http://gitea:300/`
- `http://searxng:8080/`
- `http://nextcloud-app-1:80/`

⚠️ Same caveat — these connections will disappear after a container restart. Want me to make it permanent in the compose file?
