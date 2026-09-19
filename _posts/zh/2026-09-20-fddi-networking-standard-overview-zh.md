---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FDDI网络标准概述
translated: true
type: note
---

问题：什么是网络中的FDDI？

答案：

FDDI（光纤分布式数据接口）是一种高速网络标准，使用光纤电缆在双环拓扑结构上以100 Mbps的速率传输数据。以下是其关键方面的详细说明：

**架构**

- 使用两个反向旋转的令牌环（主环和备环）以实现冗余
- 如果主环发生故障，备环会自动接管——这称为“环回绕”
- 每个网络最多支持**500个节点**，最大环长为**200公里**

**关键特性**

- 数据速率：**100 Mbps**
- 使用**令牌传递**访问方法（类似于令牌环）
- 最初设计用作连接多个局域网的**骨干网络**
- 在**物理层和数据链路层**（OSI第1层和第2层）运行

**FDDI节点类型**

- **DAS（双连接站点）**——连接到两个环；容错性更强
- **SAS（单连接站点）**——通过集中器仅连接到主环

**优势**

- 由于双环冗余，可靠性高
- 远距离覆盖（最长200公里）
- 良好的容错性和自愈能力

**局限性**

- 与以太网相比，实施成本高
- 如今已基本**过时**——被快速以太网、千兆以太网以及10GbE等现代光纤标准所取代

**（历史）使用场景**

- 校园和企业骨干网络
- 20世纪90年代需要高带宽的医学成像和CAD/CAM环境

---

参考链接：

- [FDDI – 维基百科](https://en.wikipedia.org/wiki/Fiber_Distributed_Data_Interface)
- [FDDI概述 – GeeksforGeeks](https://www.geeksforgeeks.org/fddi-full-form/)
- [网络拓扑与标准 – Cisco Press](https://www.ciscopress.com)
