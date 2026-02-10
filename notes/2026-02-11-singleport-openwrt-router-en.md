---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Single Port OpenWrt Router Solutions
translated: false
type: note
---

Question: But the sad thing is that the laptop only has one Ethernet port and no WiFi. How does that affect turning it into an OpenWrt soft router, and what are the solutions?

Answer: 

Yes, that's a common limitation with many older laptops — only one built-in Ethernet port (usually eth0 in OpenWrt) and no functional WiFi card (or unsupported by OpenWrt). This makes it tricky to have separate **WAN** (internet in) and **LAN** (your home network out) connections using just the hardware.

But it's still very doable and widely used. Here are the realistic options in order of recommendation (easiest/best first):

### 1. Best & simplest: Add a cheap USB Ethernet adapter (strongly recommended)
- Plug in one USB-to-Ethernet adapter → now you have two physical ports.
- Assign one (built-in) as WAN, the other (USB) as LAN — or vice versa.
- Most modern USB adapters work out-of-the-box or with one package install.

Popular/reliable chipsets in 2026 (good OpenWrt support):
- **Realtek RTL8153 / RTL8156** (gigabit) → install `kmod-usb-net-rtl8152`
- **ASIX AX88179** (gigabit USB 3.0)
- **TP-Link UE300 / UE306** (very common, cheap, RTL8153-based)
- Avoid very old USB 2.0-only adapters if you want gigabit speeds.

Steps after OpenWrt is installed:
1. Plug in the USB adapter.
2. SSH or LuCI → System → Software → Update lists → Search/install the driver (e.g. `kmod-usb-net-rtl8152` or `kmod-usb-net-asix`).
3. Reboot or hotplug — new interface appears (e.g. eth1).
4. Network → Interfaces → Add new interface:
   - Name: wan (or lan)
   - Protocol: DHCP client (for WAN) or static 192.168.1.1/24 (for LAN)
   - Physical: select the new eth1 (or whichever appeared)
5. Firewall → assign to wan zone (input/reject, forward/reject, masq on) or lan zone.
6. Done — now WAN on one port, LAN on the other. Connect modem/ISP to WAN port, switch/devices to LAN port.

This gives full router functionality (NAT, firewall, OpenClash/Clash, SQM, etc.) at gigabit speeds with low overhead.

### 2. Use VLANs on the single port + managed switch (more advanced, no extra hardware)
If you don't want to buy anything:
- Use a **managed/VLAN-capable switch** (e.g. cheap TP-Link TL-SG108E ~$20-30).
- Configure two VLANs on the single Ethernet port:
  - VLAN 10 = WAN
  - VLAN 1 = LAN (default)
- On the switch:
  - Port 1 (to modem/ISP) → tagged VLAN 10
  - Port 2 (to laptop's single port) → trunk/tagged VLAN 1 + 10
  - Ports 3-8 → untagged VLAN 1 (your LAN devices)
- In OpenWrt:
  - Create VLAN interfaces on eth0 (e.g. eth0.10 for WAN, eth0.1 for LAN)
  - Assign eth0.10 → wan interface (DHCP client)
  - eth0.1 (or br-lan) → lan bridge (192.168.1.1)

This works well but requires a VLAN-aware switch and more config (via LuCI: Network → Switch → add VLANs). Good for clean setups without USB.

### 3. Temporary / limited setups (not ideal for full router)
- **Use built-in port as LAN only** → connect laptop Ethernet to existing router's LAN port. OpenWrt acts as AP / proxy box / ad-blocker (no NAT, no full routing).
- **WiFi as WAN** (if card works) → but you said no WiFi.
- **USB WiFi adapter as AP** → buy USB WiFi dongle supported by OpenWrt (e.g. mt7921u chipset), use as wireless LAN AP, wired port as WAN. But USB WiFi is often less stable/powerful than built-in.

### Summary
- **Buy a $10-25 USB gigabit Ethernet adapter** → easiest path to proper dual-port router.
- Your i5 + 8GB laptop will still crush most consumer routers in performance (VPN/proxy throughput, many clients, packages).
- No WiFi? You can add a good USB WiFi adapter later for wireless AP (or use phone tethering temporarily).

Many people run exactly this setup (old laptop + USB NIC) as daily drivers for home routing/proxy in China and elsewhere.

References:  

- [OpenWrt Wiki - Single-Port Devices / VLAN setup](https://openwrt.org/docs/guide-user/network/singleportrouter)
- [OpenWrt Forum - USB Ethernet adapter drivers discussion](https://forum.openwrt.org/t/usb-2-0-to-ethernet-adapter-driver-for-openwrt/185891)
- [OpenWrt single ethernet port VLAN tutorial video reference](https://www.youtube.com/watch?v=aqvbAQmAbAU)
- [Common USB adapters for OpenWrt (TP-Link UE300 etc.)](https://nelsonslog.wordpress.com/2022/04/21/openwrt-on-raspberry-pi-4)