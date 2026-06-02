---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: STP端口状态阻塞流量
translated: true
type: note
---

问题：在 Spanning Tree Protocol (STP) 中，哪个端口状态会阻止流量以防止环路？

答案：

正确答案是 **D) Blocking**。

在 IEEE 802.1D 定义的 Spanning Tree Protocol (STP) 中，交换机端口会经历几种状态转换，以防止冗余的 Layer 2 网络中出现桥接环路。

- **Blocking**：所有端口的初始状态。在此状态下，端口**不转发任何流量**（不发送或接收用户数据帧）。它只侦听 BPDUs（Bridge Protocol Data Units）以确定网络拓扑并检测潜在环路。此状态通过阻止冗余路径上的数据流量来主动防止环路。

- **Listening**：如果端口被选中成为活动拓扑的一部分，则它会从 Blocking 状态转换到此状态。它仍然不转发用户数据，但会发送和接收 BPDUs 以参与根桥和路径选择过程。

- **Learning**：端口开始通过填充 MAC 地址表来学习 MAC 地址，但仍然不转发用户数据流量。

- **Forwarding**：最终的活动状态，端口完全参与帧转发。

Blocking 状态专门负责在拓扑收敛时阻止冗余链路上的流量以消除环路。

参考资料：

- [IEEE 802.1D 标准概述](https://www.ieee802.org/1/pages/802.1D.html)
- [Cisco Spanning Tree Protocol 端口状态文档](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html)
