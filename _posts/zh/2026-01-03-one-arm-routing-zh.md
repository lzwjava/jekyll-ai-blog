---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 单臂路由技术概述
translated: true
type: note
---

Question: What technology enables inter-VLAN communication using a single physical router interface?

Answer: 

正确答案是 **B) One-arm routing**。

One-arm routing（也称为 router-on-a-stick）允许路由器仅使用单个物理接口处理多个 VLAN 之间的通信。该接口被配置为 802.1Q trunk，并为每个 VLAN 创建逻辑 subinterfaces。每个 subinterface 都被分配了对应 VLAN 子网中的 IP 地址，路由器通过将从一个 subinterface 接收到的流量转发到另一个 subinterface 来执行 inter-VLAN routing。

- **A) Link aggregation** 是错误的——它将多个物理链路捆绑在一起以增加带宽和冗余，但不提供 inter-VLAN routing 功能。
- **C) Spanning Tree Protocol** 是错误的——它防止交换网络中的 Layer 2 环路，但在 inter-VLAN routing 中没有作用。
- **D) VRRP** 是错误的——它提供 gateway 冗余（虚拟 IP 故障转移），但不通过单个接口促进 VLAN 之间的路由。

这种配置通常用于小型网络，因为在这些网络中，为每个 VLAN 分配多个物理路由器接口是不切实际的。