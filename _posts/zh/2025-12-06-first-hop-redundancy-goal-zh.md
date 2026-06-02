---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 首跳冗余协议目标
translated: true
type: note
---

问题：First-Hop Redundancy Protocols (FHRP) 的主要目标是什么？

答案：

**B) 提供默认网关冗余**

First-Hop Redundancy Protocols (FHRP)，例如 HSRP (Hot Standby Router Protocol)、VRRP (Virtual Router Redundancy Protocol) 和 GLBP (Gateway Load Balancing Protocol)，旨在消除因 LAN 网段上的主机只有一个活动的默认网关（路由器）而导致的单点故障。它们通过允许多个物理路由器共享一个虚拟 IP 地址和虚拟 MAC 地址来实现这一点。一个路由器充当活动/主网关，而其他路由器则处于 standby 状态，如果活动路由器发生故障，它们会自动接管，确保终端设备持续的 Layer 3 连接，而无需手动重新配置。

- **A** 不正确，这不是主要目标（尽管 GLBP 确实提供了一些 load-balancing 功能，但它本质上仍然是用于冗余的 FHRP）。
- **C** 无关——FHRP 不提供 encryption。
- **D** 不正确；FHRP 实际上通过让主机向单个虚拟 MAC 地址发送 ARP 请求来减少 ARP broadcasts。

参考资料：
- [Cisco - First Hop Redundancy Protocols Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhrp-xe-16-book/fhrp-hsrp.html)
- [RFC 5798 - Virtual Router Redundancy Protocol (VRRP) Version 3](https://datatracker.ietf.org/doc/html/rfc5798)
