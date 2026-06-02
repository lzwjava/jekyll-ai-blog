---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IP 数据报内的 ICMP 详解
translated: true
type: note
---

问题：ICMP 消息在传输时封装在什么中？

答案：

ICMP（Internet Control Message Protocol）消息封装在 **IP datagrams**（或 IP packets）中进行传输。

虽然 ICMP 被视为 network layer protocol（Layer 3），用于发送有关 IP packet 处理的错误消息和操作信息，但它没有直接访问 data link layer。相反，ICMP 消息构成了 IP datagram 的 payload（数据部分）。然后，将 IP header 添加到此 payload，指定源和目标 IP addresses，然后整个单元向下传递到 data link layer 进行 framing 和传输。

Key points：
- **Protocol Number**：在 IP header 中，“Protocol” 字段设置为 **1**，以指示 payload 是 ICMP 消息。
- **Relationship**：ICMP 通常被描述为 IP 的组成部分，但逻辑上它位于 IP 之上，因为其消息承载在 IP packets 内部。
- **Structure**：`[ IP Header | ICMP Header | ICMP Data ]`

因此，您句子中的空白应填充为 **IP 数据报**（IP datagram）。

References:
