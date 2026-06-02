---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 虚电路分组交换详解
translated: true
type: note
---

Question: Packet switching 可以分为两种类型：datagram packet switching 和 ______ packet switching。

Answer:

Packet switching 是一种将数据分组为 packets 并通过数字网络传输的方法。它主要根据连接管理方式分为两种不同的方法：

1. **Datagram Packet Switching**：在这种方法中，每个 packet 被独立视为一个单独实体。每个 packet 包含完整的目的地信息，并可能采取不同的路由到达目的地。因此，packets 可能乱序到达，由接收端负责重新组装它们。这种方法是 connectionless 的。

2. **Virtual Circuit Packet Switching**：在这种方法中，在传输任何数据之前，在源和目的地之间建立一个逻辑路径（称为 virtual circuit）。特定会话的所有 packets 遵循这条相同的预定义路径。虽然没有创建物理专用线路（不同于 circuit switching），但 packets 的顺序被保留，并按顺序到达。这种方法是 connection-oriented 的。

因此，缺失的术语是 **virtual circuit**。

References:

- [Virtual Circuit vs. Datagram - GeeksforGeeks](https://www.geeksforgeeks.org/virtual-circuit-vs-datagram/)
- [Packet Switching - Wikipedia](https://en.wikipedia.org/wiki/Packet_switching)
