---
audio: false
generated: true
image: false
lang: en
layout: post
title: LAN Proxy Host Setup Complete
translated: false
type: note
---

Done! ✅ The laptop at `192.168.1.42` is now a working proxy host (no OpenWrt needed).

## What was set up

| Item | Detail |
| --- | --- |
| **Binary** | mihomo v1.19.30 (linux-amd64-v1) → `/usr/local/bin/mihomo` |
| **Config** | Copied from Mac `~/.config/mihomo/` → `/etc/mihomo/` (incl. `Rules/` providers + geoip) |
| **Service** | `mihomo.service` systemd unit, `enabled` (starts on boot), running as root with TUN |
| **Ports** | HTTP `7890`, SOCKS `7891`, Mixed `7892`, API `9090` — open to LAN via ufw |

## Two problems found & fixed along the way

1. **Wrong system clock** — the laptop's RTC battery is dead (BIOS clock said 2003), so the system time was stuck at 2026-05-25. The proxy server's TLS cert (valid from Aug 26) was rejected → all proxy connections failed. Set the clock manually from the Mac; NTP (`ntp.ubuntu.com`) now keeps it synced (offset ~1ms).
2. **ufw blocking LAN** — leftover from the OpenWrt attempt, INPUT policy was DROP. Added allow rules for `192.168.1.0/24` on ports 7890–7892 and 9090.

## Verified

- On the laptop itself: TUN mode works (traffic auto-proxied), Google/GitHub return 200, Baidu goes DIRECT
- From your Mac: `http://192.168.1.42:7892` works as a LAN-wide proxy (exit IP `69.63.219.52`, your dmit VPS)

So any device on the LAN can now just set its proxy to `192.168.1.42:7892` (or the laptop itself transparently proxies everything via TUN). The dashboard API is also reachable at `http://192.168.1.42:9090` from the LAN if you want a web UI.
