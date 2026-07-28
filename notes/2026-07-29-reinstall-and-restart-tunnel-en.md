---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reinstall and Restart Tunnel
translated: false
type: note
---

Here's the complete status of all services and how to access them from outside:

---

## 🖥️ Services Running Inside

| Service | Local Address | Port | Description |
| --------- | -------------- | ------ | ------------- |
| **Jupyter Lab** | `0.0.0.0` | **8888** | Token: `amd-oneclick`, Base URL: `/instances/u-9758-811746f0/` |
| **AHL (AI Video Generator)** | `127.0.0.1` | **8000** | Main demo app (responds 200) |
| **Tunnel Demo Page** | `127.0.0.1` | **8081** | Test page ("RC Tunnel is working") |
| **SSH** | external | **31005** | Your current access |

---

## 🔗 Demo URL (Broken)

The **RC Tunnel** (frpc) is set up to expose **AHL on port 8000** via:

```
https://rc-26cc80c1b835b7a3.radeon.firstdg.ai
```

**But it's NOT working.** The state.json shows:

```json
{
  "tunnel_id": "tun_cb197ffdbb65782284d9e6af",
  "fqdn": "rc-26cc80c1b835b7a3.radeon.firstdg.ai",
  "local_port": 8000,
  "pid": 25628
}
```

However, the frpc logs keep showing:

```
oauth2: "invalid_client" "invalid client credentials"
```

The OIDC credentials have **expired** — the token (`/var/run/secrets/frp-self-service/token`) is no longer valid for the tunnel broker.

---

## 🛠️ How to Fix — Reinstall & Restart Tunnel

Run these commands on the server to re-install and restart the tunnel:

```bash
# 1. Stop the current tunnel
export PATH="$HOME/.local/bin:$PATH"
rc-tunnel stop

# 2. Reinstall the tunnel client
/var/run/secrets/frp-self-service/install

# 3. Stop old frpc if still running
pkill -f frpc 2>/dev/null

# 4. Start a fresh tunnel exposing the demo (AHL on port 8000)
"$HOME/.local/bin/rc-tunnel" expose --port 8000
```

After that, wait ~10 seconds and check:

```bash
"$HOME/.local/bin/rc-tunnel" status
```

It will output a URL like `https://rc-<random>.radeon.firstdg.ai` — that's your public demo URL.

---

## 📌 Alternative Access (Without Tunnel)

Since you have **SSH access via port 31005**, you could also use SSH port forwarding to access services locally:

```bash
# From your machine, access Jupyter Lab locally at http://localhost:8888
ssh -L 8888:localhost:8888 -p 31005 root@36.150.116.206

# Or access AHL demo locally at http://localhost:8000
ssh -L 8000:localhost:8000 -p 31005 root@36.150.116.206
```

Then open your browser to `http://localhost:8000` for the **AI Video Generator** demo, or `http://localhost:8888/instances/u-9758-811746f0/` (token: `amd-oneclick`) for Jupyter Lab.

Want me to reinstall the tunnel and get you a working public URL?
