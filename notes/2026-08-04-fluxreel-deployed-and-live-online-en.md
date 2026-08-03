---
audio: false
generated: true
image: false
lang: en
layout: post
title: FluxReel Deployed and Live Online
translated: false
type: note
---

All verified. **FluxReel is deployed and served on the internet.** 🎉

## ✅ Final State

### Live service

| | |
| --- | --- |
| **Public URL** | **<https://rc-63980f23582dde21.radeon.firstdg.ai>** |
| Tunnel | `rc-tunnel 0.3.0`, status **active**, FRPC PID 11650 |
| Local server | `fluxreel server` (uvicorn, PID 11614) on `127.0.0.1:8081` |
| Health check | `/health` → `{"status":"ok","jobs":0,"local_models":[]}` — **HTTP 200** both locally and through the public URL |

### The web UI + API are reachable

- `/` → **FluxReel — AI Video Generator** web interface
- `/openapi.json` → FluxReel API (health, generate-content, generate-video, jobs, job status/download, check-key)

### What was done

1. **Deployed** — full rsync of the updated source to `/root/amd-hackathon-lzwjava` (editable install → live)
2. **Installed rc-tunnel** — the install script needed `FRP_BROKER_URL`/`FRP_BROKER_TLS_SERVER_NAME` exported from `/proc/1/environ` first (they're not in shell env)
3. **Started the server** bound to `127.0.0.1:8081` (per platform requirement — only 127.0.0.1 services are tunnelable)
4. **Exposed** via `rc-tunnel expose --port 8081` → platform-assigned `rc-*.radeon.firstdg.ai` URL
5. **Verified** from the internet: health 200, UI served, API docs up

### Management commands

```bash
# from the remote box (with FRP_BROKER_URL exported)
~/.local/bin/rc-tunnel status    # or logs --lines 100 / stop
tail -f /root/server.log          # server logs
```

### ⭐ Reminder (from the platform instructions)

This instance **consumes credits while running**. When you're done, destroy it: **Profile → Active Instance → red Destroy Instance button**. After destroying, the URL dies immediately and you'll need to re-install rc-tunnel + re-expose after recreating the Notebook (the 24h domain-prefix freeze applies).

Also note: the tunnel supports only one port per Pod, and the app itself has **no authentication** — the public URL is reachable by anyone, so don't expose anything sensitive through it.
