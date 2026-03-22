---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing WebSocket Connection and Origin Errors
translated: false
type: note
---

**HTTP is fine for your case** — the `ws://` error is NOT caused by using HTTP. Here's why:

- Browsers only block `ws://` when the **page itself is served over HTTPS** (mixed content blocking). Since you're accessing `http://192.168.1.36:18789` (plain HTTP), `ws://` is perfectly allowed.
- HTTPS + `wss://` would only be required if you put a reverse proxy in front that serves HTTPS.

**The real cause** is still the server-side origin check rejecting the connection and closing it immediately — that's what produces "closed before connection established." The most common causes per the search results:

1. **CORS/Origin misconfiguration** — server rejects the origin header (your case)
2. **Invalid port/host** — mismatch between what the client connects to and what the server listens on
3. **Server not configured for WebSocket upgrades**

**Check if your config changes actually saved:**

```bash
openclaw config get gateway.controlUi
```

If `allowedOrigins` or `dangerouslyDisableDeviceAuth` aren't there, re-run:

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
systemctl --user restart openclaw-gateway.service
```

Then check the gateway logs for the actual rejection reason:

```bash
journalctl --user -u openclaw-gateway.service -n 100 --no-pager | grep -i "origin\|closed\|reject\|error"
```

Sources:
- [Sentry: How to fix "WebSocket is closed before the connection is established"](https://sentry.io/answers/how-do-i-fix-the-error-websocket-is-closed-before-the-connection-is-established/)
- [wss vs ws explained — WebSocket.org](https://websocket.org/reference/wss-vs-ws/)
- [WS on HTTP vs WSS on HTTPS — APIdog](https://apidog.com/blog/ws-on-http-vs-wss-on-https/)