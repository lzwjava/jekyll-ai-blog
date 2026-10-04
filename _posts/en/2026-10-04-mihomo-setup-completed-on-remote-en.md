---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo Setup Completed on Remote
translated: false
type: note
---

Done ✅ mihomo is fully configured and running on `lzw@192.168.1.46`.

## Summary

| Item | Status |
| ------ | -------- |
| **Binary** | `/usr/local/bin/mihomo` v1.19.32 (compatible build for AMD Athlon X4 850) |
| **Config** | Copied laptop's `~/.config/mihomo/` → `/etc/mihomo/` (config.yaml, Rules/, geoip.metadb) |
| **systemd service** | `/etc/systemd/system/mihomo.service` — `active` + `enabled` (autostarts on boot) |
| **Proxy** | Working end-to-end (tested `204 OK` through `https://www.gstatic.com/generate_204`) |

## Listening ports (same as your laptop)

- `7890` — HTTP proxy
- `7891` — SOCKS5 proxy
- `7892` — Mixed HTTP+SOCKS proxy
- `9090` — RESTful API (external-controller)
- `53` — DNS (⚠️ skipped, systemd-resolved holds it — same non-fatal behavior as your laptop)

## Important notes

1. **Node selection fixed** — The config's first node "My SS 1" (`5.223.42.176:19400`) is **dead on both machines**. I switched the remote's `Proxy` group to **"My Hysteria2 2"** (matching your laptop's current selection), and verified it works (204 OK). This selection is persisted in `cache.db`.

2. **Security consideration** (same as your laptop, just FYI) — `external-controller: 0.0.0.0:9090` has **no secret/authentication** and `allow-lan: true`. Anyone on the LAN can control mihomo or use it as a proxy. If this machine is ever exposed beyond your home LAN, consider adding a `secret` to the config.

3. To manage it later:

   ```bash
   systemctl status mihomo      # check status
   systemctl restart mihomo     # restart
   mihomo -d /etc/mihomo -t     # test config validity
   ```

Would you like me to add an API `secret` for security, or adjust anything else?
