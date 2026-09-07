---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RIP路由协议基础
translated: true
type: note
---

问题：网络中的 RIP（路由信息协议）是什么？

答案：

RIP（路由信息协议）是计算机网络中使用的最早的距离矢量路由协议之一。它帮助路由器确定在 IP 网络中转发数据包的最佳路径。

**工作原理：**

- 使用 **跳数** 作为度量标准——源和目标之间的每个路由器计为一个“跳”
- 最大跳数为 **15**；跳数为 16 表示目标不可达
- 路由器每 **30 秒** 向邻居广播其整个路由表

**版本：**

| 版本 | 描述 |
|---|---|
| RIPv1 | 有类路由，不支持子网掩码，基于广播 |
| RIPv2 | 无类路由（CIDR），支持子网掩码，基于组播 |
| RIPng | 支持 IPv6 |

**优点：**
- 配置和理解简单
- 适合小型、扁平网络

**缺点：**
- 收敛速度慢（拓扑变化后需要时间更新）
- 由于最大 15 跳，扩展性受限
- 周期性全表广播导致高带宽使用
- 效率不如现代协议如 OSPF 或 EIGRP

**何时使用：**
RIP 适用于拓扑简单的小型网络。对于更大、更复杂的企业网络，通常优先选择 OSPF 或 BGP 等协议。

参考：
- [路由信息协议 - 维基百科](https://en.wikipedia.org/wiki/Routing_Information_Protocol)
- [RIP 协议概述 - Cisco](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13719-50.html)
- [RIPv2 RFC 2453 - IETF](https://datatracker.ietf.org/doc/html/rfc2453)