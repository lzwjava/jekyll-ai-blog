---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw Bind Configuration Error
translated: false
type: note
---

Question: `openclaw config set server.host 0.0.0.0` fails with `Unrecognized key: "server"` — how do I correctly configure OpenClaw to bind to `0.0.0.0`?Question: `openclaw config set server.host 0.0.0.0` fails with `Unrecognized key: "server"` — what is the correct config key to bind OpenClaw gateway to `0.0.0.0` for LAN access?

Answer:

## Root Cause

The correct config key is **`gateway.bind`**, not `server.host`. In `openclaw.json`, the gateway binding is controlled by the `gateway.bind` key, which accepts values like `loopback`, `lan`, or a custom address.

---

## Fix: Step by Step

### Step 1 — Stop the gateway first

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

---

### Step 2 — Set the correct bind key

```bash
openclaw config set gateway.bind lan
```

The gateway supports several binding modes: `loopback` (127.0.0.1 only), `lan` (local network interface), `tailnet` (Tailscale interface), and `custom` (specified address). Each non-loopback mode requires additional authentication configuration.

---

### Step 3 — Or edit `openclaw.json` directly

```bash
nano ~/.openclaw/openclaw.json
```

Change/add the gateway block:

```json
{
  "gateway": {
    "bind": "lan"
  }
}
```

If you want to specify the exact IP explicitly:

```json
{
  "gateway": {
    "bind": "0.0.0.0"
  }
}
```

Validate JSON before saving:

```bash
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

### Step 4 — Start gateway again

```bash
openclaw gateway start
```

---

### Step 5 — Verify it is now bound to `0.0.0.0`

```bash
ss -tlnp | grep 18789
```

You should see:

```
LISTEN  0.0.0.0:18789  ...  openclaw-gateway
```

---

### Step 6 — Test from your main PC browser

```
http://192.168.1.36:18789
```

---

## ⚠️ Important: Auth Token Required After Changing Bind

Non-loopback bindings mandate authentication. OpenClaw generates a new token on every restart unless you set a fixed one. To set a stable token:

```bash
openclaw config set gateway.token "your-stable-token-here"
```

When you open `http://192.168.1.36:18789` in browser, it will ask for this token. Retrieve it anytime with:

```bash
openclaw config get gateway.token
```

Or get the full dashboard URL with token included:

```bash
openclaw dashboard --no-open
```

---

## Summary of Correct Keys

| Wrong (causes error) | Correct |
|---|---|
| `server.host` | `gateway.bind` |
| `server.port` | `gateway.port` |

```bash
# Correct commands
openclaw config set gateway.bind lan
openclaw config set gateway.port 18789
openclaw config set gateway.token "your-token"
```

References:

- [OpenClaw Config Reference - ClawTank](https://clawtank.dev/blog/openclaw-config-reference)
- [OpenClaw Port Troubleshooting Guide - AI Free API](https://www.aifreeapi.com/en/posts/openclaw-port-not-listening)
- [OpenClaw 127.0.0.1:18789 Binding Guide](https://openclawconsult.com/lab/openclaw-127-0-0-1-18789)
