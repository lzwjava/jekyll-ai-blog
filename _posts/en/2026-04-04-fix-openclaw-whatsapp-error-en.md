---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw WhatsApp Proxy Error
translated: false
type: note
---

Question: How do I fix the OpenClaw gateway error "channels.whatsapp: Unrecognized key: proxy" in `~/.openclaw/openclaw.json`?

Answer:

## Root Cause

The `proxy` key under `channels.whatsapp` is **not yet a supported configuration option** in OpenClaw. As of February 2026, a feature request (Issue #23500) was filed to add proxy support for WhatsApp connections — similar to how `channels.telegram.proxy` already works — but it has not been implemented yet.

This means if you manually added `"proxy": "..."` to your `channels.whatsapp` config (perhaps inspired by the Telegram proxy config, or by following an outdated guide), OpenClaw's config validator will reject it as an unrecognized key and refuse to start.

---

## How to Fix It

### Option 1 — Run the auto-repair command (recommended first step)

```bash
openclaw doctor --fix
```

The `doctor --fix` command automatically migrates known deprecated or invalid keys. After running it, retry the gateway restart.

---

### Option 2 — Manually remove the `proxy` key from the config

1. Open the config file:

```bash
nano ~/.openclaw/openclaw.json
```

2. Find the `channels.whatsapp` section. It likely looks something like:

```json
"channels": {
  "whatsapp": {
    "proxy": "http://127.0.0.1:7890",
    ...
  }
}
```

3. **Delete the `"proxy": "..."` line entirely**, save, and exit.

4. Restart the gateway:

```bash
openclaw gateway restart
```

---

### Option 3 — Validate the config structure first

Run this to see all invalid keys before editing:

```bash
openclaw config validate
```

Then fix each reported key.

---

## Workaround for Proxy Needs (if you're in a restricted region)

Since WhatsApp proxy support is not yet implemented in OpenClaw, users in regions where WhatsApp is blocked (e.g., mainland China) should instead set system-level proxy environment variables before launching OpenClaw:

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
openclaw gateway restart
```

This routes all outbound connections (including WhatsApp WebSocket) through your proxy at the OS level, without touching the OpenClaw config file.

---

## Summary Table

| Step | Command |
| ------ | --------- |
| Auto-fix config | `openclaw doctor --fix` |
| Manual edit | Remove `"proxy"` from `channels.whatsapp` in `~/.openclaw/openclaw.json` |
| Restart gateway | `openclaw gateway restart` |
| System proxy workaround | `export http_proxy=...` before starting OpenClaw |

References:

- [Feature Request: WhatsApp proxy support (Issue #23500)](https://github.com/openclaw/openclaw/issues/23500)
- [OpenClaw Gateway Troubleshooting Flowchart](https://clawtank.dev/blog/openclaw-gateway-troubleshooting-flowchart)
- [OpenClaw Troubleshooting Guide](https://docs.openclaw.ai/gateway/troubleshooting)
- [Bug: WhatsApp channels config broken (Issue #24263)](https://github.com/openclaw/openclaw/issues/24263)
