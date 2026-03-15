---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenWrt Router Setup Guide Options
translated: false
type: note
---

**Important:** Since the router runs OpenWrt, you have two configuration options:

## **Option 1: Router as Simple Client (Recommended)**

Keep OpenWrt's `br-lan` as is (bridge of LAN ports + WiFi). Configure its **WAN interface** to get DHCP from your laptop:

1. **On OpenWrt:**
- Go to Network → Interfaces
- Edit **WAN** interface (or create new one)
- Protocol: **DHCP client**
- Physical interface: The port connected to your laptop's USB Ethernet

2. **Result:**
```
Laptop (192.168.201.1) → DHCP → OpenWrt WAN → OpenWrt LAN/WiFi devices
```
- OpenWrt gets IP like `192.168.201.50` from your laptop
- OpenWrt NATs traffic for its LAN devices
- All traffic routes through Clash proxy

## **Option 2: Router as Switch/Bridge (Advanced)**

Convert OpenWrt to bridge mode, making your laptop handle all routing/DHCP:

1. **On OpenWrt:**
- Disable DHCP server on OpenWrt
- Add USB-connected port to `br-lan` bridge
- Set OpenWrt LAN IP to static `192.168.201.2` (or disable IP entirely)

2. **Result:**
```
Laptop (192.168.201.1) → DHCP → All devices (wired+wireless)
```
- Single subnet `192.168.201.0/24`
- Your laptop handles all routing/DHCP/proxy
- OpenWrt acts as dumb AP/switch

## **Which to choose?**

**For testing/quick setup → Option 1**
- Minimal OpenWrt changes
- Works with existing OpenWrt config
- Double NAT but fine for proxy testing

**For clean network → Option 2**
- Single subnet, no double NAT
- All devices directly through Clash
- Requires more OpenWrt reconfiguration

## **Current recommendation:**

Try **Option 1** first since it's simpler. On OpenWrt:

1. Connect USB Ethernet to any LAN port on OpenWrt
2. Log into OpenWrt LuCI (web interface)
3. Network → Interfaces → Edit WAN (or create new)
4. Protocol: **DHCP client**
5. Device: Select the physical port connected to laptop
6. Firewall: Assign to **wan** zone
7. Save & Apply

Then connect a device to OpenWrt WiFi/LAN and test `curl https://api.ipify.org`

Want me to provide exact OpenWrt CLI commands instead of web interface?