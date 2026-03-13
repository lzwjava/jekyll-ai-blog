---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw Origin Error Quickly
translated: false
type: note
---

Question: OpenClaw shows "origin not allowed" error when accessing `http://192.168.1.36:18789` from another machine — how do I fix this by configuring `gateway.controlUi.allowedOrigins`?

Answer:

## Root Cause

OpenClaw has a **CORS/origin security check** on the Control UI. When you open the dashboard from a different machine (`192.168.1.100`) than the gateway host (`192.168.1.36`), the origin is blocked by default.

---

## Fix: Add Your LAN IP to `allowedOrigins`

### Step 1 — Stop the gateway

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

---

### Step 2 — Set allowed origins via config command

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'
```

If you want to allow **any machine on your LAN** (more flexible):

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789","http://192.168.1.100:18789","http://192.168.1.1:18789"]'
```

Or the simplest — **allow all origins** (OK for home LAN):

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```

---

### Step 3 — Or edit `openclaw.json` directly

```bash
nano ~/.openclaw/openclaw.json
```

Add inside the `gateway` block:

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": [
        "http://192.168.1.36:18789",
        "http://192.168.1.100"
      ]
    }
  }
}
```

To allow all (wildcard):

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

Validate JSON syntax:

```bash
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

### Step 4 — Restart gateway

```bash
openclaw gateway start
```

---

### Step 5 — Open browser on your main PC

```
http://192.168.1.36:18789
```

It should load the Control UI without the origin error now.

---

## Full Recommended `openclaw.json` Gateway Block

Here is a clean complete gateway config for your home LAN setup:

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

---

## Summary

| Config Key | Purpose |
|---|---|
| `gateway.bind` | Which interface to listen on (`lan` = LAN IP) |
| `gateway.port` | Port number (default `18789`) |
| `gateway.controlUi.allowedOrigins` | Which browser origins are allowed to open the UI |

Using `["*"]` is **safe on a home LAN** because UFW already blocks external access to port `18789`. Only devices on `192.168.1.x` can reach it.