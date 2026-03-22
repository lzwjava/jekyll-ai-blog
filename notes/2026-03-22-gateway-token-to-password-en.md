---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switching Gateway Token to Password
translated: false
type: note
---

To switch from a gateway token to a password:

**1. Set the password:**
```bash
openclaw config set gateway.auth.password "your-password"
```

**2. Set the auth mode to password:**
```bash
openclaw config set gateway.auth.mode password
```

**3. Remove the old token (optional but recommended to avoid ambiguity):**
```bash
openclaw config set gateway.auth.token ""
```

If both `gateway.auth.token` and `gateway.auth.password` are present in config, you **must** explicitly set `gateway.auth.mode` or startup will fail.

You can also set the password via environment variable instead of config:
```bash
export OPENCLAW_GATEWAY_PASSWORD="your-password"
```

For remote gateway connections specifically, use `gateway.remote.password` instead of `gateway.auth.password`.