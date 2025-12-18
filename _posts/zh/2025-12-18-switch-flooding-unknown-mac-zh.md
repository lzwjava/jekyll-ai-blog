---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换机对未知MAC地址的泛洪转发
translated: true
type: note
---

问题：在以太网交换中，当交换机收到一个目的 MAC 地址不在其 MAC 地址表中的帧时会发生什么？

答案：

当以太网交换机收到一个目的 MAC 地址是**未知**（不在其 MAC 地址表中）的帧时，它会执行**泛洪**。交换机会将该帧从**除接收帧的入端口之外的所有端口**转发出去。这确保了如果目标连接到交换机，该帧能够到达预期的目标，同时允许交换机在收到回复时学习目标的端口。

这种行为是 Layer 2 交换机在**未知单播**情况下运行的基础。

- **选项 A** 不正确：交换机不会丢弃帧；丢弃会中断与未知目标的连接。
- **选项 B** 是正确的：从除入端口之外的所有端口泛洪。
- **选项 C** 不正确：发送到默认网关是 Layer 3（路由器）功能，而不是 Layer 2 交换机功能。
- **选项 D** 不正确：无限期缓冲不是标准行为；交换机立即转发帧。

正确答案是 **B**。

参考文献：

- [Cisco - Understanding and Configuring the Switch CAM Table](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/12013-17.html)
- [IEEE 802.1D - Media Access Control (MAC) Bridges](https://standards.ieee.org/ieee/802.1D/5001/)