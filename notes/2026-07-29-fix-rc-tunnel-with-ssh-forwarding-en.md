---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix RC Tunnel with SSH Forwarding
translated: false
type: note
---

Here's the full situation:

---

## ❌ RC Tunnel — Cannot Be Fixed on This Pod

**Root cause:** This is an old Notebook pod created **before the tunnel feature was enabled**. The platform never injected `FRP_BROKER_URL`, so:
- The install script refuses to run
- The previous client credentials (`krXGr4aWPwFUYOzWQgLPOX13xL2-Zn5-mtBcqkWq2_g`) have **expired** (`invalid_client`)
- A new client cannot be registered from inside the pod

The platform docs confirm: *"Close and recreate the Notebook, then try again."*

---

## ✅ Working Alternative — SSH Port Forwarding

Run these commands **from your local machine** to access the services immediately:

### AI Video Generator (AHL Demo) — Port 8000
```bash
ssh -L 8000:localhost:8000 -p 31005 root@36.150.116.206 -N
```
Then open: **http://localhost:8000**

### Jupyter Lab — Port 8888
```bash
ssh -L 8888:localhost:8888 -p 31005 root@36.150.116.206 -N
```
Then open: **http://localhost:8888/instances/u-9758-811746f0/** (token: `amd-oneclick`)

### Tunnel Demo Page — Port 8081
```bash
ssh -L 8081:localhost:8081 -p 31005 root@36.150.116.206 -N
```
Then open: **http://localhost:8081**

> 💡 Add `-f` to run in background, e.g. `ssh -f -L 8000:localhost:8000 -p 31005 root@36.150.116.206 -N`

---

## 🔄 To Get a Public URL (Proper Fix)

You'd need to **recreate the Notebook** from the platform console — close this pod and launch a new one. After that, the tunnel will work automatically:

```bash
/var/run/secrets/frp-self-service/install
rc-tunnel expose --port 8000
```

Want me to set up the SSH port forwarding for you now?
