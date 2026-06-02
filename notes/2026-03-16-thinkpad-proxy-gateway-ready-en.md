---
audio: false
generated: true
image: false
lang: en
layout: post
title: ThinkPad Proxy Gateway Ready
translated: false
type: note
---

**✅ Setup Complete!**

Here's what's configured on your ThinkPad:

1. **IP Forwarding** - Enabled (`net.ipv4.ip_forward=1`)
2. **NAT Masquerade** - Added for `enp2s0` (your WAN interface)
3. **USB Ethernet** - Configured as `enx00e04c362f89` with static IP `192.168.201.1/24`
4. **DHCP Server** - dnsmasq running, will serve IPs `192.168.201.50-150` to clients
5. **Clash Meta** - Installed at `/usr/local/bin/clash-meta` (v1.19.21)
6. **Basic Config** - Created at `~/.config/clash/config.yaml` with TUN mode enabled
7. **Systemd Service** - Ready at `/etc/systemd/system/clash.service`

**Next steps:**

1. **Connect a device** to the USB Ethernet port
2. **Start Clash**: `sudo systemctl start clash`
3. **Enable auto-start**: `sudo systemctl enable clash`
4. **Add your actual proxy config** to `~/.config/clash/config.yaml`

The device should get an IP like `192.168.201.50` and all traffic will route through Clash → WAN.

Want me to start Clash now or help with proxy configuration?
