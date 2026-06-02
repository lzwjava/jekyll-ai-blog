---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 虚拟局域网技术史
translated: true
type: note
---

## VLAN 历史简介

**虚拟局域网 (VLAN)** 是一项允许网络管理员在 OSI 模型的第 2 层（数据链路层）将物理网络在逻辑上划分为多个隔离广播域的技术。这使得设备可以根据功能、部门或安全需求进行分组，而无需物理分离或额外的布线。

VLAN 技术起源于 20 世纪 80 年代早期。随着以太网网络的规模不断扩大，广播流量成为一个显著问题，消耗带宽并降低性能。贝尔实验室（Bellcore）的计算机工程师 W. David Sincoskie（在早期对以太网上的语音进行实验后）被认为是 20 世纪 80 年代中期 VLAN 概念的发明者。他的工作通过创建虚拟分段来限制广播域，同时保持高速交换，解决了以太网扩展的挑战。

在 **20 世纪 90 年代早期到中期**，供应商开始实施专有的 VLAN 解决方案。Cisco 推出了 Inter-Switch Link (ISL)，这是一个通过封装以太网帧在交换机之间中继多个 VLAN 的协议。其他公司，如 3Com，也有自己的协议（例如，Virtual LAN Trunk）。这些专有方法允许 VLAN 跨多个交换机，但缺乏跨供应商的互操作性。

为了解决这个问题并提供一个标准化、多供应商的解决方案，IEEE 制定了 **802.1Q 标准**，并于 **1998 年**首次发布。该标准引入了 VLAN 标记：一个插入到以太网帧头部的 4 字节标签，包括一个 12 位 VLAN ID（支持多达 4096 个 VLAN）和优先级字段。它成为 VLAN Trunk 的主要方法，取代了大多数专有协议。

自 1998 年以来，IEEE 802.1Q 经过多次修订（例如，2004 年、2014 年的整合），增加了提供商桥接（用于 QinQ 双重标记的 802.1ad）等功能，并改进了大规模网络。VLAN 在现代网络中仍然是一个基础，在企业、数据中心和云环境中增强了安全性、性能和可管理性。

参考文献：

- [VLAN - Wikipedia](https://en.wikipedia.org/wiki/VLAN)
- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [W. David Sincoskie - Wikipedia](https://en.wikipedia.org/wiki/W._David_Sincoskie)
- [The History Behind VLANs - Real Time Automation](https://www.rtautomation.com/rtas-blog/the-history-behind-vlans/)
