---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 802.1Q VLAN标记详解
translated: true
type: note
---

问题：在VLAN上下文中，802.1Q 是什么意思？

回答：

**IEEE 802.1Q** 是定义 **VLAN 标记**在以太网网络中如何工作的网络标准。它允许单个物理网络链路同时承载来自多个 VLAN 的流量。

---

**工作原理：**

802.1Q 在以太网帧头部的源 MAC 地址和 EtherType 字段之间插入一个 **4 字节（32 位）标签**。该标签包含：

| 字段 | 大小 | 描述 |
| --- | --- | --- |
| TPID | 16 位 | 标签协议标识符 — 始终为 `0x8100`，用于标识为 802.1Q 帧 |
| PCP | 3 位 | 优先级代码点 — 用于 QoS/流量优先级 |
| DEI | 1 位 | 丢弃合格指示符 — 标记在拥塞时可丢弃的帧 |
| VID | 12 位 | **VLAN ID** — 标识帧所属的 VLAN（0–4095） |

---

**关键概念：**

- **VLAN ID 范围：** 0–4095（12 位），其中 0 和 4095 被保留，因此可用 VLAN 为 **4094 个**
- **Trunk 端口：** 交换机之间的链路传输带标签的帧，以便两端都知道帧属于哪个 VLAN
- **Access 端口：** 终端设备（PC、服务器）通常看不到标签——交换机会自动添加/移除标签
- **Native VLAN：** 每个 trunk 上可以指定一个 VLAN 为"本地"VLAN，其帧以 **未标记** 方式发送

---

**简而言之：** 802.1Q 是由 IEEE 定义的通用标准，通过将 VLAN 成员信息直接嵌入每个以太网帧中，使 VLAN 能够跨不同厂商的交换机实现互操作。

参考：

- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [VLAN Tagging Explained - Cisco](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/layer2/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_Layer_2_Switching_Configuration_Guide/b_Cisco_Nexus_9000_Series_NX-OS_Layer_2_Switching_Configuration_Guide_chapter_0100.html)
- [IEEE 802.1Q Standard Overview](https://standards.ieee.org/ieee/802.1Q/10323/)
