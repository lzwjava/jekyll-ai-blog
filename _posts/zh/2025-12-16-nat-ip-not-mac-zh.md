---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: NAT转换IP地址而非MAC地址
translated: true
type: note
---

问题：网络地址转换是否用于将 IP 地址转换为 MAC 地址，反之亦然？

回答：

不，那是不正确的。

**网络地址转换 (NAT)** 是一种网络技术，用于在数据包通过路由器或防火墙时修改数据包头中的 IP 地址（通常还有端口）。其主要目的是：

- 允许多个私有网络（使用私有 IP 地址）上的设备共享单个公共 IP 地址以访问互联网。
- 节省公共 IPv4 地址。
- 通过隐藏内部 IP 地址提供一定程度的安全性。

NAT 在 OSI 模型的**网络层 (Layer 3)** 运行，仅处理 **IP 地址**（在 Port Address Translation 或 PAT/NAT overload 的情况下还处理端口）。它完全不涉及 MAC 地址。

你描述的过程——在 **IP 地址**和 **MAC 地址**之间进行转换——由**地址解析协议 (ARP)** 处理，该协议在**数据链路层 (Layer 2)** 运行。ARP 将 IPv4 地址解析为本地网络段内的 MAC 地址，而反向 ARP (RARP) 或类似机制可以执行相反的操作（尽管 RARP 已基本过时）。

总结：

- NAT：IP ↔ IP（和端口）
- ARP：IP → MAC（在本地网络上）

这些是针对不同层和目的的不同协议。

参考文献：

- [Network address translation - Wikipedia](https://en.wikipedia.org/wiki/Network_address_translation)
- [What Is Network Address Translation (NAT)? - Cisco](https://www.cisco.com/site/us/en/learn/topics/networking/what-is-network-address-translation-nat.html)
- [Does NAT change the source MAC address? - Server Fault](https://serverfault.com/questions/145876/does-nat-change-the-source-mac-address)
- [Does NAT Map to the MAC Address, or to the Local IP? - Super User](https://superuser.com/questions/651143/does-nat-map-to-the-mac-address-or-to-the-local-ip)
