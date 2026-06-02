---
audio: false
generated: true
image: false
lang: en
layout: post
title: WhatsApp Proxy Setup Recap
translated: false
type: note
---

Here's the summary, Boss:

---

## WhatsApp Setup — Recap

**What worked:** Plugin installed, QR scanned successfully, WhatsApp linked and connected.

**What was painful:**

1. **Proxy is mandatory** — Server's direct network can't sustain WhatsApp WebSocket connections (408 timeout). Standard `HTTP_PROXY`/`HTTPS_PROXY` env vars in the systemd service did nothing for Baileys WebSocket.

2. **proxychains4 was the real fix** — It intercepts all TCP at the libc level, forcing everything (including Node's WebSocket) through mihomo. Had to use `socks5 127.0.0.1 7891` (SOCKS port, not HTTP 7890).

3. **Gateway needs proxychains too** — The systemd service had to be updated to wrap the gateway process with `proxychains4`, otherwise WhatsApp disconnects after restart.

4. **QR code relay was too slow** — By the time I sent the QR to webchat and you read it, it had cycled multiple times. You ended up SSH'ing in directly to scan — that's the only reliable way.

**Config changes made:**
- Installed `@openclaw/whatsapp` plugin
- Added `channels.whatsapp` config with `dmPolicy: "pairing"`
- Updated systemd service to wrap with `proxychains4`
- Proxy config: `/etc/proxychains4.conf` → `socks5 127.0.0.1 7891`

Noted for next time. 🦞
