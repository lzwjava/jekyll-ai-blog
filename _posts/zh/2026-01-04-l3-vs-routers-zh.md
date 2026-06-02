---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 三层交换机与传统路由器
translated: true
type: note
---

Question: What is the main difference between Layer 3 switches and traditional routers?

1. Layer 3 switches differ from traditional routers mainly because they:
   A) Use hardware-based fast forwarding for routing
   B) Only support static routing
   C) Cannot perform NAT
   D) Operate only at Layer 2

Correct answer: A

Answer:

Layer 3 switches 与传统 routers 之间的主要区别在于它们的转发机制。

Layer 3 switches 使用专用硬件（通常是 ASICs - Application-Specific Integrated Circuits）来执行 inter-VLAN routing 和 IP forwarding，从而能够以极低的延迟实现 wire-speed 的 routing 性能。这种基于硬件的转发（通常被称为使用类似 CEF 表的 "route once, switch many"）使得它们在处理大流量的内部网络流量时比传统 routers 快得多。

传统 routers，尤其是基于软件的 routers，传统上依赖 CPU 处理每个 packet 的 routing 决策，与硬件加速相比速度较慢。

其他选项解析：

- **B) Only support static routing**: 错误。现代 Layer 3 switches 支持 dynamic routing protocols（在某些情况下支持 OSPF, EIGRP, RIP, BGP）。
- **C) Cannot perform NAT**: 虽然基础的 Layer 3 switches 通常缺乏完整的 NAT 功能（常见于企业级 access/distribution layers），但许多高端型号确实支持 NAT。这不是*主要*区别。
- **D) Operate only at Layer 2**: 错误。Layer 3 switches 同时在 Layer 2 (switching) 和 Layer 3 (routing) 运行。

因此，最关键的区别特征是 **hardware-based fast forwarding for routing**，这使得选项 **A** 成为正确选择。
