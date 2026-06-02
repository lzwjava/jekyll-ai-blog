---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 网络链路聚合的好处
translated: true
type: note
---

Question: What is the primary benefit of link aggregation?

Answer:

The correct answer is **B) It increases bandwidth and provides redundancy on backbone links**。

Link aggregation（在 Cisco 术语中也称为 EtherChannel，或 LACP/IEEE 802.1AX）将多个物理 Ethernet 链路组合成一个逻辑链路。这主要实现了两个关键优势：

- **Increased bandwidth**：流量在绑定的链路之间进行 load-balanced，从而实现比单一链路更高的聚合 throughput。
- **Redundancy/fault tolerance**：如果一条物理链路失效，流量会重新分配到剩余的链路上，从而防止 outage。

其他选项错误的原因是：
- **A)** 防止 network loops 是 Spanning Tree Protocol (STP) 的功能，而不是 link aggregation。
- **C)** 自动 IP 地址分配由 DHCP 处理。
- **D)** 交换机之间的流量 encryption 由 MACsec 等协议提供，而不是 link aggregation。
