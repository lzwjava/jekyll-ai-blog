---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Unreachable on Port 22
translated: false
type: note
---

Port 22 on `165.245.135.10` is refusing connections — it's not accepting SSH at all regardless of username. Only port 80 (HTTP) is open.

```
PORT   STATE SERVICE
80/tcp open  http
```

Your SSH config routes non-local IPs through a SOCKS5 proxy (localhost:7891), but even through the proxy, port 22 is closed on that host.

A few possibilities:
- The firewall/security group on the server doesn't allow port 22
- SSH is on a non-standard port (I scanned ~15 common alternatives — none open)
- The server might be down or SSH service not running
- You may need a VPN or jump host to reach it

You able to check the server's firewall or let me know what port SSH is actually on?
