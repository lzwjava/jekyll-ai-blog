---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Favicon、证书、DNS、仓库均已同步
translated: true
type: note
---

Done ✅

```
087a97f nginx: serve favicon set (apple-touch-icon, fun-live-icon/) on mobile vhosts
pushed: 8c3e5cb..087a97f  master -> github.com:lzwjava/live-server.git
working tree: clean
VM nginx.conf == repo HEAD: IN SYNC
```

**本次会话工作的最终状态：**
- 🔒 `https://funlive.io/?#/lives` — 已修复（证书 SAN `funlive.io, www.funlive.io`，已验证 200，`ssl_verify=0`）
- 🌐 DNS — 已移除多余的 Namecheap URL 转发记录，仅保留 `34.150.108.243`
- 🔄 证书续期 — `certbot renew --dry-run` 通过，每日 cron 覆盖两个证书
- 📦 仓库 — `nginx.conf`、`docker-compose.yml`、`deploy/renew-certs.sh` 已从虚拟机同步，以及 favicon 差异；全部已提交并推送