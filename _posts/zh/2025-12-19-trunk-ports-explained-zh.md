---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 中继端口详解
translated: true
type: note
---

问题：交换机中的 trunk port 是什么？

答案：

网络交换机上的 **trunk port** 是一种特殊类型的端口，配置为通过单个物理链路承载**多个 Virtual Local Area Network (VLAN)** 的流量。这与**access port** 不同，access port 专用于单个 VLAN，通常连接到计算机或打印机等终端设备。

### trunk port 的主要特点：
- **多 VLAN 支持**：它允许来自不同 VLAN 的帧通过链路传输（例如，在两个交换机之间或从交换机到路由器）。
- **VLAN Tagging**：为了区分来自不同 VLAN 的流量，trunk port 使用**标记**。最常见的标准是 **IEEE 802.1Q**，它在以太网帧头中插入一个 4 字节的标签，其中包含 VLAN ID (VID)。这确保了接收设备知道帧属于哪个 VLAN。
- **Native VLAN**：trunk port 通常有一个“native VLAN”（在 Cisco 设备上通常默认是 VLAN 1）。native VLAN 的帧以**未标记**的方式发送，而其他帧则被标记。这提供了与不支持标记的设备的向后兼容性。
- **常见用途**：
  - 连接交换机以在多个设备之间扩展相同的 VLAN。
  - 将交换机连接到路由器（例如，在用于 VLAN 间路由的“router-on-a-stick”设置中）。
  - 连接到理解 VLAN 标签的设备，例如 IP 电话、具有多个虚拟机的服务器或广播多个 SSID 的 access point。

### trunk port 与 access port：

| 特性                 | Access Port                          | Trunk Port                              |
|----------------------|--------------------------------------|-----------------------------------------|
| 支持的 VLAN          | 仅单个 VLAN                          | 多个 VLAN                               |
| 标记                 | 未标记帧（交换机在内部添加/移除标签） | 已标记帧（使用 802.1Q 或旧式 ISL）      |
| 典型连接             | 终端设备（PC、打印机等）             | 交换机、路由器或支持标签的设备          |
| 帧处理               | 将所有流量分配给一个 VLAN            | 承载并分离许多 VLAN 的流量              |
| 安全考虑             | 更简单，隔离到一个 VLAN              | 风险更高（例如，如果配置不当可能发生 VLAN hopping）；使用 pruning 来限制允许的 VLAN |

trunk port 通过减少对多根物理电缆的需求使网络更高效——一个 trunk link 可以取代每个 VLAN 的许多单独链接。但是，它们需要仔细配置以避免安全问题或路由错误。

参考资料：

- [JumpCloud: What Is a Trunk Port?](https://jumpcloud.com/it-index/what-is-a-trunk-port)
- [N-able: VLAN Trunking Overview](https://www.n-able.com/blog/vlan-trunking)
- [GeeksforGeeks: Access and Trunk Ports](https://www.geeksforgeeks.org/computer-networks/access-trunk-ports/)
- [Network Engineering Stack Exchange: Purpose of Trunk Port](https://networkengineering.stackexchange.com/questions/40668/what-is-the-purpose-of-a-trunk-port-in-a-network-switch)
- [Cisco Press: Trunk Links](https://www.ciscopress.com/articles/article.asp?p=29803&seqNum=3)
