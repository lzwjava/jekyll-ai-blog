---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 校园网子网规划指南
translated: true
type: note
---

Question: 1. In subnet planning, what is essential for a medium-sized campus network?
A) Using only public IP addresses
B) Proper IP address subnetting and allocation
C) Assigning the same subnet to all departments
D) Avoiding VLANs entirely

2. (The provided answer is B)

Answer:

### Question 1

正确答案是 **B) Proper IP address subnetting and allocation**。

在中型 campus network 中，有效的 subnet 规划对于高效利用 IP address 空间、提高网络性能、增强安全性和简化管理至关重要。合理的 subnetting 包括根据组织需求（例如按部门、建筑或功能）将大型网络划分为更小的逻辑子网（subnets）。这样做可以实现：

- 更好的流量分段并减少 broadcast domains。
- 可扩展的增长和高效的 IP 利用（特别是通过 RFC 1918 使用 private IPv4 addresses）。
- 与 VLANs 集成以实现 Layer 2 隔离和 Layer 3 routing。
- 应用 access controls 和 QoS 策略。

**为什么其他选项是错误的：**

- **A) Using only public IP addresses**: Public IPs 资源有限且昂贵；campus networks 通常使用 private IP addresses 并配合 NAT 进行互联网访问。
- **C) Assigning the same subnet to all departments**: 这会创建一个巨大的单一 broadcast domain，导致拥塞、安全风险和较差的可管理性。
- **D) Avoiding VLANs entirely**: VLANs 通常与 subnetting 结合使用，在不需要额外物理基础设施的情况下提供逻辑隔离。

### Question 2

如上所述，提供的答案 **B** 是正确的。

References:

- [Cisco Campus Network Design Basics](https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/campover.html)
- [RFC 1918 - Address Allocation for Private Internets](https://tools.ietf.org/html/rfc1918)
