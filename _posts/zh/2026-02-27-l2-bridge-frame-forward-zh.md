---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网桥在二层转发帧
translated: true
type: note
---

问题：在 OSI seven-layer reference model 中，bridge 在 data link layer 工作，它实现的转发功能是：

A. Bit forwarding
B. Frame forwarding
C. Packet forwarding
D. Message forwarding

答案：

**B. Frame forwarding**

**解释：**

**bridge** (网桥) 是 OSI 模型中 **Layer 2** (**Data Link Layer**) 工作的网络设备。

在 data link layer，protocol data unit (PDU) 称为 **frame** (帧)。

因此，bridge 根据 frame header 中包含的 MAC addresses 做出转发决策，并将整个 **frames** 从一个 segment 转发到另一个。

- **Bit forwarding** (A)：这不是标准术语，不对应任何真实 layer 的转发行为。
- **Packet forwarding** (C)：这是由 routers 执行的，它们在 **Layer 3** (Network Layer) 工作，其中 PDU 是 **packet** (包含 IP headers)。
- **Message forwarding** (D)："Message" 是更通用/应用层术语，不用于 data link layer 转发的上下文中。

正确答案：**B. Frame forwarding** (帧转发)

bridge 读取 frame 中的 destination MAC address，在其 MAC address table（也称为 forwarding table 或 CAM table）中查找，并决定从哪个 port 输出 frame —— 这是经典的 **frame forwarding**。

参考文献：

- 无（来自 OSI model 和 IEEE 802.1D bridging specification 的标准网络知识）
