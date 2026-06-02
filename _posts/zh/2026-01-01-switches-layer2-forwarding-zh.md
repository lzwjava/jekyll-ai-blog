---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换机与 OSI 第二层转发
translated: true
type: note
---

Question: Switches 主要在 OSI 的哪一层进行基本转发？

Answer:

Switches 主要在 OSI model 的 **Layer 2 (Data Link Layer)** 运行，用于实现基本转发。

### Explanation

OSI (Open Systems Interconnection) model 是一个将网络系统功能标准化的概念框架，共分为七层。以下是与 switches 相关的简要概述：

- **Layer 1 (Physical Layer)**：处理数据的物理传输（例如：cables, signals）。Hubs 等设备在此层运行，但它们只是简单地广播数据，没有智能。
- **Layer 2 (Data Link Layer)**：处理 framing、error detection 以及基于 **MAC (Media Access Control) addresses** 的转发。这是 basic switches 功能所在的层——它们学习连接设备的 MAC addresses，并仅将 frames 转发到目标 port，从而减少网络拥塞。
- **Layer 3 (Network Layer)**：涉及基于 IP addresses 的 routing。Routers 在此层运行，但一些高级的 "Layer 3 switches" 也可以在网络之间进行 route。
- **Layer 4 (Transport Layer)**：管理端到端通信（例如：TCP/UDP）。对于 basic switching 并不相关。

对于 **basic forwarding**，switches 使用 MAC addresses 来做出决策，这属于 Layer 2 功能。它们为每个 port 创建独立的 collision domains，但将设备保持在同一个 broadcast domain 中（除非配置了 VLANs）。

### Why Not the Other Options?

- **A) Layer 1**：错误——Layer 1 设备（如 hubs）不会进行智能转发；它们只是将信号复制到所有 ports。
- **C) Layer 3**：对于 basic switches 是错误的——Layer 3 涉及 IP routing。虽然存在 Layer 3 switches，但它们是在 Layer 2 switching 的基础上增加了 routing 功能。
- **D) Layer 4**：错误——此层用于 transport protocols，而不是像 switches 这样的转发硬件。

### Real-World Example

在小型办公室 LAN 中，switch 连接电脑和打印机。当 Computer A 向 Computer B 发送数据时，switch 会检查 MAC address 并将 frame 直接发送到 B 的 port，而不会向所有设备广播（这与 hub 不同）。

如果你正在准备认证考试（例如：CCNA），请记住：基础 Ethernet switches 是 Layer 2 设备。

References:

- [Network Switch - Wikipedia](https://en.wikipedia.org/wiki/Network_switch)
- [Layer 2 vs Layer 3 Switches - GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/difference-between-layer-2-and-layer-3-switches/)
- [What is a Network Switch? - Network World](https://www.networkworld.com/article/969239/what-is-a-network-switch-and-how-does-it-work.html)
