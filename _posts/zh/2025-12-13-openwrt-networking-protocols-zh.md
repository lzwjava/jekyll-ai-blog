---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OpenWrt支持的网络协议
translated: true
type: note
---

问题：OpenWrt实现了哪些协议或拥有哪些协议？

答案：

OpenWrt 是一个基于 Linux 的开源固件，用于路由器等嵌入式设备。它不实现单一的特定协议，而是通过其核心 Linux 内核、配置系统 (UCI/network config) 和可安装软件包 (通过 opkg) 支持广泛的网络协议。

支持的协议主要类别：

- **基本 IP 和连接协议**（内置或核心）：
  - 静态 IP
  - DHCP（客户端和服务器）
  - DHCPv6
  - PPPoE, PPPoA
  - IPv4 和 IPv6（完整的双栈支持，包括 VLAN）

- **隧道和 VPN 协议**（通过 /etc/config/network 中的软件包和协议处理程序）：
  - WireGuard (现代、高性能 VPN)
  - OpenVPN
  - L2TP (通过 xl2tpd 软件包)
  - PPTP (通过 ppp-mod-pptp 软件包)
  - GRE (通过 gre 软件包)
  - VXLAN
  - IPsec (ESP, AH, ISAKMP 通过防火墙规则)

- **蜂窝/调制解调器协议**：
  - QMI, MBIM, NCM, PPP (用于 4G/LTE 调制解调器)

- **其他网络功能**：
  - UPnP, NAT-PMP, PCP (用于端口转发)
  - Spanning Tree Protocol (STP)
  - Relay (用于伪桥接)

OpenWrt 的可扩展性允许通过数千个可用软件包添加更多协议。许多都需要安装特定的软件包（例如，OpenVPN 需要 openvpn-openssl）。

参考资料：

- <https://openwrt.org/docs/guide-user/network/tunneling_interface_protocols>
- <https://en.wikipedia.org/wiki/OpenWrt>
- <https://sternumiot.com/iot-blog/openwrt-how-it-works-challenges-and-alternatives/>
- <https://teklager.se/en/knowledge-base/openwrt-4g-wwan-configuration/>
