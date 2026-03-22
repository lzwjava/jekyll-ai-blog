---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bypass Device Auth for Plain HTTP
translated: false
type: note
---

You need to set `gateway.controlUi.dangerouslyDisableDeviceAuth=true` to bypass the secure context requirement over plain HTTP:

```bash
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
```

Then restart:

```bash
systemctl --user restart openclaw-gateway.service
```

This disables device identity checks and relies on your token/password auth instead. It's flagged as dangerous in the audit output, but is the intended escape hatch for plain HTTP on a trusted LAN. Turn it off if/when you add HTTPS (e.g. via a reverse proxy with a cert).