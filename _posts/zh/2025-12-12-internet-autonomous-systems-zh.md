---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 互联网自治系统解析
translated: true
type: note
---

问题：互联网上的自治系统 (AS) 是什么？

答案：

自治系统 (AS) 是互联网的基本组成部分，由受单一管理实体（例如 ISP、大学、公司或政府机构）控制的大型网络或网络组构成。每个 AS 管理一系列 IP 路由前缀，并采用统一、明确定义的路由策略来确定它如何与其他 AS 交换流量。

主要方面包括：

- **自治系统号 (ASN)**：每个公共 AS 都由一个唯一的 ASN 标识，该 ASN 由 IANA 监管下的区域互联网注册机构 (RIR) 分配。最初是 16 位（最大 65,535），在 2007 年扩展到 32 位以适应增长，目前已分配超过 100,000 个 ASN。

- **在路由中的作用**：AS 使用边界网关协议 (BGP) 来公布其 IP 地址空间并与相邻 AS 交换路由信息。数据包通过在 AS 之间跳跃穿梭，直到到达目标 AS，然后由目标 AS 在内部传输。

- **AS 的类型**：
  - **Stub/Single-homed**：仅连接到一个其他 AS（通常是最终用户网络）。
  - **Multihomed**：连接到多个 AS 以实现冗余，但不转发流量。
  - **Transit**：在其他 AS 之间传输流量（ISP 常见）。

这种去中心化的结构使得全球互联网能够作为“网络的网络”运行，实现了高效的、基于策略的路由，而无需单一的中央机构。

参考资料：

- [What is an autonomous system? | Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Autonomous system (Internet) - Wikipedia](https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29)
- [Autonomous System Numbers - ARIN](https://www.arin.net/resources/guide/asn/)
- [What are autonomous systems and how do they work? | TechTarget](https://www.techtarget.com/searchnetworking/definition/autonomous-system)
