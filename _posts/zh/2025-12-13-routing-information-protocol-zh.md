---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 路由信息协议简介
translated: true
type: note
---

问题：全面介绍路由信息协议 (RIP)。

答案：

### 概述
路由信息协议 (RIP) 是计算机网络中最古老的距离矢量路由协议之一。它是一种内部网关协议 (IGP)，设计用于在单个自治系统内进行路由。RIP 使路由器能够交换路由信息，以确定转发数据包的最佳路径，主要使用跳数作为其路由度量——数据包到达目的地所经过的路由器数量。

RIP 在 UDP 端口 520 上运行，并基于 Bellman-Ford 算法。它配置简单，适用于中小型网络，但其局限性使其不适合大型复杂环境。

### 历史
RIP 起源于网关信息协议 (GWINFO)，由施乐公司于 1970 年代中期为其实验网络开发。它演变为施乐网络系统 (XNS) RIP，影响了 Novell 的 IPX RIP 和 AppleTalk 的 RTMP 等协议。

RIP 的 IP 版本于 1982 年在 Berkeley Software Distribution (BSD) UNIX 中作为“routed”守护程序实现。1988 年，RIPv1 通过 RFC 1058 进行了标准化。

### 版本
主要有三个标准化版本：

- **RIPv1** (RFC 1058, 1988)：
  一种有类路由协议，在更新中不包含子网掩码信息。它使用广播更新（到 255.255.255.255）且缺乏身份验证。路由仅由 IP 目的地和跳数决定。

- **RIPv2** (RFC 2453, 1998；废止了早期的 RFC，如 1723 和 1388)：
  一种无类协议，支持可变长子网掩码 (VLSM)、无类域间路由 (CIDR) 和路由汇总。它引入了组播更新（到 224.0.0.9）以提高效率，支持身份验证（纯文本或 MD5），并增加了一个路由标签字段。它保持与 RIPv1 的向后兼容性。

- **RIPng** (RIP Next Generation, RFC 2080)：
  IPv6 网络的扩展，类似于 RIPv2，但使用 128 位地址和 UDP 端口 521 上的组播组 ff02::9。它不包含身份验证（而是依赖 IPsec）。

不存在标准的 RIPv3；RIPng 作为 IPv6 的适配版本。

### RIP 如何工作
RIP 路由器维护一个路由表，其中包含目的地、度量（跳数）和下一跳的条目。

- **更新**：路由器定期（默认每 30 秒）向邻居发送其整个路由表。
- **度量**：跳数；直接连接网络的度量为 0。最大跳数为 15（16 表示不可达，防止无限循环）。
- **路径选择**：首选跳数最低的路由。
- **收敛**：使用触发更新进行更改，但依赖“计数到无穷大”来解决环路，导致收敛速度较慢。

防止环路和不稳定性发生的关键机制：
- **水平分割 (Split Horizon)**：不要将从某个接口学习到的路由再通告回该接口。
- **路由毒化 (Route Poisoning)**：将失败路由的度量标记为 16。
- **抑制定时器 (Hold-Down Timers)**：当一个路由变得不可达后，在一段时间内（默认 180 秒）忽略对其的更新。
- **毒性反转 (Poison Reverse)**：通过通告被毒化的路由来覆盖水平分割。

定时器（典型默认值）：
- 更新 (Update)：30 秒
- 无效 (Invalid)：180 秒（如果在 180 秒内没有收到更新则将路由标记为不可用）
- 抑制 (Hold-down)：180 秒
- 清除 (Flush)：240 秒（移除路由）

RIP 的管理距离为 120，使其不如 OSPF (110) 或 EIGRP (90) 等协议受欢迎。

### 优点
- 配置和操作简单。
- CPU 和内存使用率低。
- 广泛支持，易于理解，适用于教育目的。

### 缺点
- 限制为 15 跳，不适用于大型网络。
- 收敛速度慢（计数到无穷大问题）。
- 每 30 秒进行完整表广播/组播，导致带宽使用率高。
- RIPv1 缺乏安全性和子网支持。
- 不考虑带宽、延迟或负载，只考虑跳数。

### 当前状态（截至 2025 年）
由于更好的可扩展性和功能，RIP 在企业和大型网络中已H广泛被 OSPF、IS-IS、EIGRP 和 BGP 等高级协议取代。然而，它仍用于：
- 小型、简单的网络。
- 遗留系统。
- 教育和实验室环境，以教授路由基础知识。

它对于理解距离矢量原理和在受限设置中偶尔部署仍然具有重要意义。

参考资料：

- [Wikipedia: Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol)
- [RFC 1058: Routing Information Protocol](https://datatracker.ietf.org/doc/html/rfc1058)
- [RFC 2453: RIP Version 2](https://datatracker.ietf.org/doc/html/rfc2453)
- [GeeksforGeeks: Routing Information Protocol (RIP)](https://www.geeksforgeeks.org/computer-networks/routing-information-protocol-rip/)
- [Cisco Community: RIP (Routing Information Protocol)](https://community.cisco.com/t5/networking-knowledge-base/rip-routing-information-protocol/ta-p/5007445)
