---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 帧中继合并数据链路层
translated: true
type: note
---

问题：在 Frame Relay 中，交换设备中的 layers 概念通过合并 data link layer 和 network layer 而简化。

（判断该陈述是真还是假，并从参考答案视角填写正确的层名称。）

答案：

该陈述是 **true**。

Frame Relay 确实在交换设备上“淡化/简化”了严格的 layering 概念，通过合并/结合 **data link layer** (Layer 2) 和 **network layer** (Layer 3) 的功能。

空白处正确的填写词是 **数据链路** (data link)。

### 解释

传统的 packet-switched networks（如 X.25）明确分离：

- Layer 2: LAPB (framing, error control, flow control)
- Layer 3: X.25 PLP (virtual circuit management, routing, multiplexing)

Frame Relay 从网络中移除了大部分 Layer 3 功能（特别是在 carrier network 内部）。Frame Relay switches 仅查看帧头中的 DLCI (Data Link Connection Identifier) 来转发帧——这本质上是 Layer 2 的 forwarding decision。

然而，DLCI 具有类似于 Layer 3 virtual circuits 的 multiplexing 和 virtual circuit 意义。因此，Frame Relay 通常被描述为“merged”或“blurred the boundary”了 data link layer 和 network layer 之间。

因此，许多 Chinese teaching materials 中的标准 textbook 描述是：

Frame Relay淡化了交换设备上的层次概念，将**数据链路层**和网络层进行了融合。

空白处应填写 **数据链路** (or 数据链路层)。

参考文献：

- None (standard knowledge in computer networking textbooks, especially in Chinese higher education materials for computer networks)
