---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing WebSocket Origin Check Rejected Error
translated: false
type: note
---

The WS is being closed immediately because the origin check is still rejecting it. The browser sends `Origin: http://192.168.1.36:18789` with the WS upgrade, and it must match `allowedOrigins` exactly.

Run both fixes together:

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
```

Then restart:

```bash
systemctl --user restart openclaw-gateway.service
```

The origin must be the **exact** origin string the browser sends — scheme + host + port, no trailing slash. Since you're on `http://192.168.1.36:18789`, that's the value.

If you want to allow any client on your LAN without listing IPs individually, use `"*"`:

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```