---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 内部网关协议详解
translated: true
type: note
---

问题：什么是内部网关协议？

回答：

内部网关协议（IGP）是一类路由协议，用于在单个**自治系统（AS）**内的路由器之间交换路由信息。自治系统是指在共同管理下的一个网络或一组网络，例如企业网络或ISP网络。

IGP使路由器能够动态发现和维护路由，以实现AS内部高效的数据包转发，并使用带宽、延迟或跳数等度量指标来确定最佳路径。

### 主要特点

- **范围**：仅限于一个AS。
- **与EGP对比**：与处理互联网上不同AS之间路由的外部网关协议（例如BGP）不同，IGP仅关注内部路由。

### 主要的IGP类型

IGP通常分为三类：

- **距离向量协议**
  路由器与其邻居共享其整个路由表，使用简单的度量指标（例如跳数）。
  示例：**路由信息协议（RIP）**——简单但可扩展性有限（最多15跳）。

- **链路状态协议**
  路由器洪泛链路状态通告以构建完整的网络拓扑图，然后计算最短路径（例如，通过Dijkstra算法）。收敛速度更快，可扩展性更好。
  示例：
  - **开放最短路径优先（OSPF）**——广泛使用，支持大型网络。
  - **中间系统到中间系统（IS-IS）**——类似于OSPF，常用于ISP环境。

- **混合/高级距离向量协议**
  结合了距离向量的简单性与链路状态的特性，以实现更快的收敛。
  示例：**增强型内部网关路由协议（EIGRP）**——最初是思科专有协议，现已开放标准；使用复合度量指标。

截至2025年，最常见的IGP仍然是OSPF、IS-IS和EIGRP，而RIP主要用于小型或传统网络。

参考文献：

- [Interior gateway protocol - Wikipedia](https://en.wikipedia.org/wiki/Interior_gateway_protocol)
- [Understanding Interior Gateway Protocol (IGP) - JumpCloud](https://jumpcloud.com/it-index/understanding-interior-gateway-protocol-igp)
- [Routing: IGP and EGP Protocols | Baeldung on Computer Science](https://www.baeldung.com/cs/routing-igp-egp-protocols)
- [IGP, EGP, and Autonomous System Explained](https://www.computernetworkingnotes.com/ccna-study-guide/igp-egp-and-autonomous-system-explained.html)
