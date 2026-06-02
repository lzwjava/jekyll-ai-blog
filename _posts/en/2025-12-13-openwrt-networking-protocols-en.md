---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OpenWrt Supported Networking Protocols
translated: false
type: note
---

Question: What protocol does OpenWrt implement or have?

Answer:

OpenWrt is a Linux-based open-source firmware for embedded devices like routers. It does not implement a single specific protocol but supports a wide range of networking protocols through its core Linux kernel, configuration system (UCI/network config), and installable packages (via opkg).

Key categories of protocols supported:

- **Basic IP and connection protocols** (built-in or core):
  - Static IP
  - DHCP (client and server)
  - DHCPv6
  - PPPoE, PPPoA
  - IPv4 and IPv6 (full dual-stack support, including VLANs)

- **Tunneling and VPN protocols** (via packages and protocol handlers in /etc/config/network):
  - WireGuard (modern, high-performance VPN)
  - OpenVPN
  - L2TP (with xl2tpd package)
  - PPTP (with ppp-mod-pptp package)
  - GRE (with gre package)
  - VXLAN
  - IPsec (ESP, AH, ISAKMP via firewall rules)

- **Cellular/modem protocols**:
  - QMI, MBIM, NCM, PPP (for 4G/LTE modems)

- **Other networking features**:
  - UPnP, NAT-PMP, PCP (for port forwarding)
  - Spanning Tree Protocol (STP)
  - Relay (for pseudo-bridging)

OpenWrt's extensibility allows adding more protocols via thousands of available packages. Many require installing specific packages (e.g., openvpn-openssl for OpenVPN).

References:

- <https://openwrt.org/docs/guide-user/network/tunneling_interface_protocols>
- <https://en.wikipedia.org/wiki/OpenWrt>
- <https://sternumiot.com/iot-blog/openwrt-how-it-works-challenges-and-alternatives/>
- <https://teklager.se/en/knowledge-base/openwrt-4g-wwan-configuration/>
