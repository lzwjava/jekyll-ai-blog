---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw WhatsApp Mihomo Proxy Setup
translated: false
type: note
---

Question: How do I make OpenClaw's WhatsApp channel work in China using a Mihomo proxy on port 7890?

Answer:

## Root Cause

WhatsApp is blocked in mainland China, and while Telegram already supports proxy configuration via `channels.telegram.proxy`, WhatsApp currently does **not** have a native proxy option in OpenClaw. This is a known open feature request.

The `status=408 Request Time-out WebSocket Error` you see is because the Baileys WebSocket connection to WhatsApp Web servers is blocked — even though `curl` via your system `http_proxy` env vars works fine, setting environment variables like `http_proxy` does not guarantee that Node.js apps will use them — when an application uses its own explicit proxy config, it bypasses the system proxy tunnel entirely. Always test at the application layer.

---

## Current Workaround Options

### Option 1: Verify Mihomo is Actually Listening

First, confirm what ports are actually open:

```bash
for port in 1080 1087 1086 7890 7891 8080 8118 10808 10809; do
  nc -zv 127.0.0.1 $port 2>&1 | grep -v refused
done
```

Mihomo (like ClashX, Clash Verge, or Mihomo Party) exposes a local SOCKS5 port (default: 7891) and an HTTP proxy port (default: 7890), which is exactly what OpenClaw expects.

### Option 2: Use `ALL_PROXY` / `GLOBAL_AGENT_HTTP_PROXY` for Node.js

Standard `http_proxy` env vars are often ignored by Node.js WebSocket libraries. Try forcing a global proxy for Node.js before launching:

```bash
export ALL_PROXY=http://127.0.0.1:7890
export GLOBAL_AGENT_HTTP_PROXY=http://127.0.0.1:7890
openclaw channels login --channel whatsapp
```

Or with SOCKS5 (port 7891 in Mihomo):

```bash
export ALL_PROXY=socks5://127.0.0.1:7891
openclaw channels login --channel whatsapp
```

### Option 3: Use `proxychains` to Force All Traffic Through Proxy

Install and configure `proxychains-ng`:

```bash
sudo apt install proxychains4

# Edit /etc/proxychains4.conf
# Change the last line to:
socks5  127.0.0.1  7891
# or http:
http    127.0.0.1  7890
```

Then run:

```bash
proxychains4 openclaw channels login --channel whatsapp
```

This forces all TCP connections from OpenClaw (including WebSocket) through your Mihomo proxy.

### Option 4: Set Mihomo to "TUN Mode" (Global Proxy)

In Mihomo/Clash Verge, enable **TUN Mode** (also called "System Proxy" or "Global Mode"). This routes all traffic at the OS network level, so Node.js WebSockets are also proxied without any app-level configuration.

- Open Mihomo/Clash Verge UI → enable **TUN Mode** or set mode to **Global**
- Then run `openclaw channels login --channel whatsapp` normally

---

## Long-Term Fix (Pending)

A feature request has been filed to add a `channels.whatsapp.proxy` config option, similar to how Telegram proxy already works. The proposed solution is to pass a `ProxyAgent` from `undici` to the Baileys `makeWASocket` function via the `fetchAgent` option. Once this is merged, you'll be able to simply run:

```bash
openclaw config set channels.whatsapp.proxy "http://127.0.0.1:7890"
```

Until then, **TUN mode** or **proxychains** are the most reliable workarounds.

---

## Also: Fix the Duplicate Plugin Warning

Your `nextcloud-talk` plugin warning is unrelated to the connection issue, but you can fix it by removing the bundled conflict — either delete the custom extension or explicitly set it in your config:

```bash
openclaw config set plugins.allow '["nextcloud-talk", "openclaw-weixin"]'
```

This suppresses the auto-load warning and makes your plugin list explicit.

References:

- [Feature request: WhatsApp proxy support (GitHub Issue #23500)](https://github.com/openclaw/openclaw/issues/23500)
- [Bug report: same 408 error with WSL2 + proxy (GitHub Issue #7885)](https://github.com/openclaw/openclaw/issues/7885)
- [OpenClaw Telegram China proxy debugging guide](https://www.xugj520.cn/en/archives/openclaw-telegram-china-proxy-fix.html)