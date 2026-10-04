---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo v1.19.32 Installed
translated: false
type: note
---

Done ✅ mihomo v1.19.32 is installed on `lzw@192.168.1.46`.

## Summary

| Item | Value |
|------|-------|
| **Binary** | `/usr/local/bin/mihomo` |
| **Version** | Mihomo Meta v1.19.32 (linux amd64, go1.26.8) |
| **Build** | `compatible` — chosen because the remote CPU (AMD Athlon X4 850) lacks AVX2 |
| **Method** | Downloaded locally → SCP → `sudo install` (since the remote couldn't reach GitHub directly) |

Verified: the binary runs correctly on the remote CPU and `mihomo -v` reports the right version.

## Notes / next steps (not yet done)

The binary is installed, but mihomo is **not yet configured or running as a service**:

- ❌ No config file at `/etc/mihomo/config.yaml`
- ❌ No systemd service (so it won't autostart)

To make it actually work you'll need a proxy config (subscription URL or custom rules). Want me to:

1. **Create `/etc/mihomo/config.yaml`** — paste a config or give me a subscription URL, and
2. **Set up a systemd service** so it runs on boot?

Just let me know how you'd like to proceed.