---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 局域网广播传输基础
translated: true
type: note
---

问题：局域网（LANs）的一般传输方法是什么？

答案：

正确答案是 **广播** (broadcast)。

**解释：**

在传统的 LANs（尤其是使用集线器或早期总线拓扑的 Ethernet）中，数据链路层最常见和基本的传输方法是 **broadcast**。

主要特点：
- 当设备发送数据帧时，该帧会传输到同一本地网络段上的**所有设备**。
- LAN 上的所有设备都会接收该帧。
- 只有 MAC 地址与帧中目标地址匹配的设备才会处理它，其他设备则丢弃它。

这就是为什么 LANs 通常被描述为使用 **broadcast transmission**（或广播域内的“一对所有”传输）。

常见相关概念：
- **Unicast**（单播）：one-to-one（在知道目标 MAC 后实际数据传输最常见）
- **Broadcast**（广播）：one-to-all（用于 ARP、DHCP、发现协议等）
- **Multicast**（组播）：one-to-many（特定组）

但是当教科书或考试问题询问局域网的 **general / typical transmission method** 时，尤其是在经典 Ethernet LANs 的上下文中，标准答案是 **广播方式** (broadcast mode)。

尽管现代交换式 Ethernet 通过 MAC 地址学习和转发大大减少了不必要的 broadcast 流量，但 LAN broadcast domain 的本质仍然存在，经典/典型的描述仍使用 "broadcast"。

所以参考答案 **广播** 是正确的。

参考文献：
无
