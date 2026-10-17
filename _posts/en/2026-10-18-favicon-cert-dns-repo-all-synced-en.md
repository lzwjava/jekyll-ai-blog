---
audio: false
generated: true
image: false
lang: en
layout: post
title: Favicon, cert, DNS, repo all synced
translated: false
type: note
---

Done ✅

```
087a97f nginx: serve favicon set (apple-touch-icon, fun-live-icon/) on mobile vhosts
pushed: 8c3e5cb..087a97f  master -> github.com:lzwjava/live-server.git
working tree: clean
VM nginx.conf == repo HEAD: IN SYNC
```

**Final state of this session's work:**

- 🔒 `https://funlive.io/?#/lives` — fixed (cert SAN `funlive.io, www.funlive.io`, verified 200, `ssl_verify=0`)
- 🌐 DNS — stray Namecheap URL-forward record removed, only `34.150.108.243` remains
- 🔄 Cert renewal — `certbot renew --dry-run` passes, daily cron covers both certs
- 📦 Repo — `nginx.conf`, `docker-compose.yml`, `deploy/renew-certs.sh` synced from VM, plus the favicon drift; all committed and pushed
