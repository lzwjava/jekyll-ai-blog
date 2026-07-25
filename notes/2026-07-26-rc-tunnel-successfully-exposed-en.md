---
audio: false
generated: true
image: false
lang: en
layout: post
title: RC Tunnel Successfully Exposed
translated: false
type: note
---

Everything is working perfectly! Here's the full summary:

---

## ✅ RC Tunnel Successfully Exposed

### 📋 What was done

| Step | Status |
|------|--------|
| **Env vars extracted** from `/proc/1/environ` | ✅ Found `FRP_BROKER_URL` & `FRP_BROKER_TLS_SERVER_NAME` |
| **`rc-tunnel` installed** | ✅ v0.3.0 → `~/.local/bin/rc-tunnel` |
| **Test page created** | ✅ `~/tunnel-demo/index.html` |
| **HTTP server started** | ✅ Python3 on `127.0.0.1:8081` |
| **Local test** | ✅ `curl` returned the HTML page |
| **Tunnel exposed** | ✅ via `rc-tunnel expose --port 8081` |

### 🌐 Public URL

```
https://rc-a899e6bb9beab78e.radeon.firstdg.ai
```

### 🔍 Verification

- **Public URL reachable** — both local and remote `curl` return:
  ```html
  <!doctype html><title>RC Tunnel</title><h1>RC Tunnel is working</h1>
  ```
- **Status:** `active`, FRPC PID `1140`, proxy logged in and healthy
- **Server logs** show successful login and proxy startup

### ⚠️ Note

The `status` and `logs` subcommands require the same env vars (`FRP_BROKER_URL`, `FRP_BROKER_TLS_SERVER_NAME`) to be exported. You can source them from `/proc/1/environ` or add them to your shell profile.

### 🛑 To stop the tunnel

```bash
# With env vars exported:
export FRP_BROKER_URL=$(grep -z FRP_BROKER_URL /proc/1/environ | tr '\0' '\n' | cut -d= -f2-)
export FRP_BROKER_TLS_SERVER_NAME=$(grep -z FRP_BROKER_TLS_SERVER_NAME /proc/1/environ | tr '\0' '\n' | cut -d= -f2-)
export PATH="$HOME/.local/bin:$PATH"
rc-tunnel stop
```
