---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configure Gateway Allowed Origins
translated: false
type: note
---

The config key is `gateway.controlUi.allowedOrigins`. You can either list specific origins or use `"*"` to allow all.

For your LAN setup, set it via:

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.1", "http://192.168.1.2"]'
```

Or to allow **any** origin (wildcard — simpler for a trusted LAN):

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```

Note: `"*"` disables origin allowlisting entirely (the audit will warn about it, but it won't block startup). For a private LAN this is usually acceptable.

After updating, restart the gateway:

```bash
systemctl --user restart openclaw-gateway.service
```