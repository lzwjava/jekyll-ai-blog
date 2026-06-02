---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: VLAN 技术的用途与优势
translated: true
type: note
---

Question: What is the main purpose of VLAN technology?

A) To increase broadcast domains
B) To segment the network and isolate traffic between different departments
C) To improve routing speed across WANs
D) To encrypt data packets

Answer:

The correct answer is **B**。

VLAN (Virtual Local Area Network) 技术的主要目的是在不需要独立的物理 Switch 或基础设施的情况下，将一个物理网络逻辑地划分为多个隔离的 broadcast domains。这使得不同 VLAN 中的设备即使连接到同一台 Switch，也可以实现流量隔离（包括 broadcasts）。它通常用于隔离不同部门之间的流量、提高安全性、减少 broadcast 开销并增强网络管理。

- 选项 A 是错误的，因为 VLAN 实际上是**减少**（或分割）了 broadcast domains——一个 VLAN 等于一个 broadcast domain。
- 选项 C 是错误的，因为 VLAN 运行在 Layer 2（LAN 内部），不会直接影响跨越 WANs（Layer 3 广域网连接）的 routing speed。
- 选项 D 是错误的，因为 VLAN 不提供加密功能；它们仅通过 VLAN IDs 对 frames 进行标记以实现 segmentation（加密由 IPsec 或 WPA 等其他 protocols 处理）。

综上所述，VLAN 在 data link layer 提供流量隔离和 network segmentation，因此 B 是正确选项。
