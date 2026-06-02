---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling Global Bind for OpenClaw Gateway
translated: false
type: note
---

Question: How do I change the OpenClaw gateway config from "loopback" (127.0.0.1) to bind globally (0.0.0.0) so it's accessible via 192.168.1.36:18789?

Answer:

## Simple Config Change

Just change **two fields** in your config:

```json
"gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
        "mode": "token",
        "token": "86c230696f27eada444097a03167fca718b3321b3d52c117"
    }
}
```

**Change to:**

```json
"gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "all",
    "auth": {
        "mode": "token",
        "token": "86c230696f27eada444097a03167fca718b3321b3d52c117"
    }
}
```

---

## What Changed

| Field | Before | After | Meaning |
|---|---|---|---|
| `bind` | `"loopback"` | `"all"` | Listen on `0.0.0.0` instead of `127.0.0.1` |

> The typical values are `loopback` → binds to `127.0.0.1` only, and `all` → binds to `0.0.0.0` (all interfaces).
> Some configs use `global` instead of `all` — check OpenClaw's own documentation if `all` doesn't work.

---

## After Changing

1. **Save** the config file
2. **Restart** the OpenClaw service:

```bash
systemctl restart openclaw
# or
pkill openclaw && openclaw &
```

3. **Verify** it's now listening on all interfaces:

```bash
ss -tlnp | grep 18789
# Should show: 0.0.0.0:18789  (not 127.0.0.1:18789)
```

4. **Allow firewall** if needed:

```bash
sudo ufw allow 18789
```

5. Access from your browser:

```
http://192.168.1.36:18789
```

---

## Security Note

⚠️ Since your config already has **token auth** enabled (`"mode": "token"`), you are protected — any request must include the token. This is fine for LAN use, but **do not expose port 18789 to the public internet** without additional firewall rules.
