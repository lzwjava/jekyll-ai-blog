---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VLAN与Trunk详解
translated: true
type: note
---

问题：什么是VLAN，什么是Trunk（网络中的）？

答案：

**VLAN（虚拟局域网）**

VLAN 是将一个物理网络逻辑划分为多个独立的广播域。即使设备连接到同一台物理交换机，VLAN 也能让它们像处于不同网络中一样分组。关键点：

- 每个 VLAN 拥有自己的 ID（例如 VLAN 10、VLAN 20）
- 一个 VLAN 中的流量必须经过路由器或三层交换机才能到达另一个 VLAN
- 提高安全性，减少广播流量，简化网络管理
- 示例：在同一台物理交换机上隔离人力资源、财务和工程部门

**Trunk（Trunk链路）**

Trunk 是一种网络链路，可以在交换机、路由器或其他网络设备之间**同时承载多个 VLAN** 的流量。关键点：

- 使用标签协议（最常见的是 **IEEE 802.1Q**）为每个数据帧标记其 VLAN ID
- 允许一根物理电缆同时传输多个 VLAN
- 通常用于交换机之间或交换机与路由器之间的连接
- Trunk 的对立面是**Access端口**，它仅承载单个 VLAN 的流量

**简单类比**

| 概念 | 类比 |
| --- | --- |
| VLAN | 高速公路上的单独车道 |
| Trunk | 承载所有车道的高速公路本身 |

参考资料：

- [IEEE 802.1Q – VLAN标记](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [Cisco – VLAN概述](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/vlans.html)
- [Cisco – Trunking概念](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html)
