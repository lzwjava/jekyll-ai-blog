---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 统一 AS 路由策略
translated: true
type: note
---

**问题：** 什么术语填入空白——一个 Autonomous System (AS) 可以使用多个内部 routing protocols 和 metrics，但它向其他 AS 呈现一个 ________ 和一致的 routing policy？

**答案：**

答案是 **单一的 (single / unified)**。

---

### 解释

一个 **Autonomous System (AS)** 被定义为一个由单一行政实体控制的 IP 网络和路由器集合。其关键原则是：

**内部**，一个 AS 可以非常复杂：

- 它可以运行多个 Interior Gateway Protocols (IGPs)，如 OSPF、EIGRP、RIP 或 IS-IS。
- 它可以为内部路由选择使用不同的 metrics（hop count、bandwidth、delay、cost 等）。
- 它可以有数千台配置各异的路由器。

**外部**，然而，一个 AS 必须将自身呈现为一个单一的、统一的实体：

- 一个 autonomous system (AS) 是一个大型网络或网络组，具有 **unified routing policy**。每个连接到 Internet 的计算机或设备都连接到一个 AS。

- 一个 Autonomous System (AS) 是一个由单一实体控制的 IP 网络和路由器集合，**向 internet 呈现 unified routing policy**。

- 一个 AS 是一个网络或一组由一个或多个网络运营商控制的连接的 IP routing prefixes，**向 internet 呈现 common routing policy**。

这种“单一的/统一的”routing policy 就是 AS 通过 **BGP (Border Gateway Protocol)**——Internet 上不同 AS 之间使用的 exterior gateway protocol——向其他 AS 公布的内容。

### 为什么这很重要？

| Aspect | Internal (Inside AS) | External (To other ASes) |
| --- | --- | --- |
| Routing Protocol | Multiple IGPs (OSPF, RIP, EIGRP…) | Single EGP (BGP) |
| Routing Policy | Can vary by region/department | One unified policy |
| Metrics | Different per protocol | Abstracted into BGP attributes |
| Identity | Many routers, many subnets | One ASN (e.g., AS13335) |

Policy decisions（如优先选择某些网络路径、接受或拒绝来自特定来源的路由）**保持在 AS 内部，对外部系统不可见**。这正是 Internet 能够扩展的原因——每个 AS 处理自己的内部复杂性，并仅向外暴露一个干净的、单一的 routing policy。

**因此，空白应填入：单一的 (single)**

---

**参考资料：**

- [Cloudflare — What is an Autonomous System?](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Kentik — BGP Routing Tutorial](https://www.kentik.com/kentipedia/bgp-routing/)
- [CacheFly — BGP Routing Guide](https://www.cachefly.com/news/a-guide-to-border-gateway-protocol-bgp-routing-and-its-applications/)
- [JumpCloud — What is an Autonomous System?](https://jumpcloud.com/it-index/what-is-an-autonomous-system-as)
