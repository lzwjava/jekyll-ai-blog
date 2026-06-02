---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网桥接功能与操作
translated: true
type: note
---

问题：什么是以太网桥？它是如何工作的？

回答：

**以太网桥**（也称为网络桥）是一种第二层（数据链路层）网络设备，它将多个以太网网络段连接到一个逻辑网络中。它根据 MAC 地址过滤和转发以太网帧，与集线器或中继器相比，能减少不必要的流量和冲突。

### 主要特点

- 在 **OSI 第二层**运行，使用 MAC 地址（不像路由器那样使用 IP 地址）。
- 创建一个**广播域**，但分离了**冲突域**。
- 对设备是“透明的”——终端站感知不到它的存在。
- 历史上用于将以太网网络扩展到超出电缆长度限制的范围，或用于对流量进行分段以提高性能。
- 现代等效设备：多端口桥演变为**网络交换机**（交换机本质上是具有硬件加速的高端口数网桥）。

### 工作原理

以太网桥使用称为**透明桥接**（IEEE 802.1D 标准）的过程，包括学习、转发、过滤和泛洪：

1. **学习**：
    - 网桥维护一个**转发表**（MAC 地址表或 CAM 表）。
    - 当帧到达某个端口时，网桥会将其**源 MAC 地址**和接收端口记录到表中。
    - 如果长时间（通常为 300 秒）未刷新，表项将过期。

2. **转发/过滤**：
    - 对于传入帧，网桥检查**目的 MAC 地址**。
    - 如果目的 MAC 地址在表中且在不同的端口上，则仅将帧**转发**到该端口。
    - 如果目的 MAC 地址在同一个入站端口上，则**过滤**（丢弃）该帧——无需转发。
    - 这通过仅在需要时发送流量来减少网络拥塞。

3. **泛洪**：
    - 如果目的 MAC 地址未知、是广播或多播，网桥会将帧**泛洪**到除入站端口之外的所有端口。

4. **环路预防**：
    - 使用**生成树协议 (STP)** 检测并阻断冗余路径，防止在环形拓扑中出现广播风暴。

### 示例

- 网段 A：包含 MAC A1、A2 的设备（连接到端口 1）。
- 网段 B：包含 MAC B1、B2 的设备（连接到端口 2）。
- 设备 A1 向 B1 发送一个帧。
- 网桥看到源 A1 → 学习到 A1 在端口 1。
- 目的 B1 未知 → 泛洪到端口 2。
- B1 回复 → 网桥学习到 B1 在端口 2，并将未来的流量直接转发。

实际上，网桥在早期的以太网网络中很常见，但已大部分被交换机取代，交换机以更快速度和更多端口执行相同功能。

参考文献：

- [Network bridge - Wikipedia](https://en.wikipedia.org/wiki/Network_bridge)
- [Bridges - How Ethernet Works | HowStuffWorks](https://computer.howstuffworks.com/ethernet12.htm)
- [What is a Network Bridge? - CBT Nuggets](https://www.cbtnuggets.com/blog/technology/networking/what-is-network-bridge)
- [Network bridge explained - Study CCNA](https://study-ccna.com/network-bridge-explained/)
