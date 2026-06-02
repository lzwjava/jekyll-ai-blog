---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 策略驱动域间路由
translated: true
type: note
---

问题：Internet 的规模如此庞大，以至于 autonomous systems 之间的路由非常困难，因此 inter-AS routing 优先考虑（）。

答案：

**策略** (policy) / **策略优先** / **政策优先**

**解释：**

Internet 由数千个独立的 **Autonomous Systems (AS)** 组成，每个属于不同的组织（ISPs、universities、大型公司、content providers 等），并且每个都有自己的商业利益、安全要求、成本考虑和业务关系（customer、peer、provider）。

因为这些差异，**ASes 之间的路径选择不能简单使用最短路径或最佳性能指标**（如同 intra-domain routing protocols 如 OSPF/IS-IS 中的那样）。相反，最重要的因素通常是 **routing policy**（或 routing strategy / policy-based routing）。

**BGP (Border Gateway Protocol)** —— inter-domain routing 的 de facto 标准 —— 本质上是一个 **policy-based** routing protocol。它的主要工作不是找到技术上“最佳”的路径，而是允许每个 AS 实施自己的 **preferred policies**，例如：

- 优先 customer routes 而非 peer routes 而非 provider routes
- 避免免费转交通信（peering disputes）
- 优先更便宜的链路
- 出于安全或法律原因优先避免某些国家/地区的路径
- 执行 traffic engineering 目标
- 为安全起见 blackhole 或过滤特定 prefixes

因此，正确答案是 **策略** (policy) 或 **政策** (policy)，并且在中国教材和考试中最常见的表述是：

**自治系统之间的路由选择是策略优先**
or
**策略优先** / **政策优先**

**参考文献：**

- 无（标准的计算机网络知识，BGP 核心概念）
