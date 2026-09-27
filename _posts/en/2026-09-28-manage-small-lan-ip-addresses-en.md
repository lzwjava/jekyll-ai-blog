---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manage Small LAN IP Addresses
translated: false
type: note
---

Question: In a small LAN with about 5–10 computers, how do I manage the network — see what IP each device has, and what tools should I use?

Answer:

For a network that small, you don't need enterprise-grade tools. A simple, practical setup:

**1. Give every device a known, stable IP**
- Easiest: set up **DHCP reservations** on your router (most home/small-office routers support this in their admin page, usually at 192.168.1.1 or 192.168.0.1). This lets devices still use DHCP but always get the same IP based on their MAC address.
- Alternative: assign **static IPs** manually on each device, staying outside your router's DHCP range to avoid conflicts.

**2. See what's currently connected**
- **Router's admin page** — almost all routers have a "connected devices" or "DHCP client list" page showing IP, MAC address, and hostname.
- **Nmap** (free, cross-platform) — run `nmap -sn 192.168.1.0/24` to scan the whole subnet and list live hosts.
- **Fing** (mobile/desktop app) — very easy GUI for scanning your LAN, shows device names, vendors, and IPs.
- **Angry IP Scanner** — free, simple GUI scanner, good for Windows/Mac/Linux.

**3. Keep track of assignments over time**
- For just 5–10 machines, a simple spreadsheet (hostname, MAC, assigned IP, purpose) is honestly enough.
- If you want something more automated, tools like **Pi-hole** (also does ad-blocking + DNS) can show a live list of devices and let you assign local hostnames.

**4. Optional: centralized management**
- If these are work computers you want to monitor/administer remotely, something like **TeamViewer**, **AnyDesk**, or setting up a lightweight **NAS with network monitoring** (e.g., Synology/QNAP dashboard) can help, but this may be overkill for 5–10 machines.

**Suggested minimal setup:** router DHCP reservations + Fing or Nmap for occasional scans + a spreadsheet log. That covers "what IP is what device" cleanly without extra infrastructure.

References:
- [Nmap Official Site](https://nmap.org/)
- [Fing Network Scanner](https://www.fing.com/)
- [Angry IP Scanner](https://angryip.org/)
- [Pi-hole](https://pi-hole.net/)
