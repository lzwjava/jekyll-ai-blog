---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: VLAN 划分第 2 层广播域
translated: true
type: note
---

问题：VLAN 在交换网络中的主要目的是什么？

答案：
VLAN（虚拟局域网）的主要目的是**分割 Layer 2 广播域**。

在一个没有 VLAN 的标准交换网络中，连接到同一个交换机（或互连交换机）的所有设备都属于一个单一的广播域——每个广播帧都会泛洪到所有端口。通过在交换机上创建多个 VLAN，可以在逻辑上将其划分为单独的广播域。来自一个 VLAN 的广播流量被限制在该 VLAN 内，不会到达其他 VLAN 中的设备，即使它们可能共享相同的物理基础设施。这提高了安全性，减少了不必要的流量，并允许更好的网络组织。

- **A) 增加广播域大小** → 不正确。VLAN 实际上通过分割广播域来减小每个广播域的有效大小。
- **B) 分割 Layer 2 广播域** → 正确。
- **C) 替代路由器的需要** → 不正确。VLAN 间通信仍然需要 Layer 3 设备（路由器或 Layer 3 交换机）。
- **D) 提供 Layer 3 加密** → 不正确。VLAN 在 Layer 2 运行，不提供加密。

因此，正确答案是 **B**。
