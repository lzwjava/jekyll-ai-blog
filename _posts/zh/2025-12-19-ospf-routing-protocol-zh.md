---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OSPF路由协议类型
translated: true
type: note
---

问题：OSPF 属于哪种路由协议？

答案：

OSPF (Open Shortest Path First) 是一种 **链路状态 (Link State)** 路由协议。

### 解释

- **链路状态 (Link State)** 协议（如 OSPF 和 IS-IS）在整个路由域中泛洪详细的拓扑信息（链路状态）。每台路由器都构建一个完整的网络地图，并使用 Dijkstra 的最短路径优先 (SPF) 算法来计算到达所有目的地的最佳路径。
- 相反：
  - **距离矢量 (Distance Vector)** 协议（例如 RIP，经典模式下的 EIGRP）只与邻居共享距离度量和下一跳信息，而没有完整的拓扑可见性。
  - **路径矢量 (Path Vector)** 协议（例如 BGP）交换完整的路径属性（AS 路径）以防止域间路由中的环路。
  - **混合 (Hybrid)** 协议（有时用于描述 EIGRP）结合了距离矢量和链路状态的元素，但并非纯粹的链路状态协议。

因此，正确答案是 **B) 链路状态 (Link State)**。

（注意：选项 A 不正确，因为它适用于 RIP 等协议。）
