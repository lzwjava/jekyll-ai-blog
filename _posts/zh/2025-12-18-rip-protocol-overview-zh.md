---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 网络中的RIP协议概述
translated: true
type: note
---

### RIP 协议简介
**路由信息协议（RIP）** 是计算机网络中最古老、最简单的动态路由协议之一。它是一种**距离矢量路由协议**，作为**内部网关协议 (IGP)** 运行，这意味着它用于在单个自治系统 (AS) 内交换路由信息。RIP 使用**跳数**（数据包必须经过的路由器数量）作为其唯一的度量标准来确定到目标网络的最佳路径。最大跳数限制为 **15**，**16** 表示网络不可达。这一限制使得 RIP 主要适用于中小型网络。

RIP 基于 **Bellman-Ford 算法**，最初开发于 20 世纪 80 年代，从 Xerox 网络中的 Gateway Information Protocol (GWINFO) 等早期协议演变而来。

### RIP 如何工作
RIP 路由器维护一个路由表，其中包含已知网络的条目，包括目的地、度量标准（跳数）和下一跳路由器。

- **定期更新**：每隔 **30 秒**，路由器将其整个路由表发送给相邻路由器。
- **传输**：使用 **UDP 端口 520**。
- **更新机制**：路由器交换完整的路由表（被称为“谣言路由”，因为路由器信任来自邻居的信息）。
- **收敛**：更新传播后网络达到稳定状态，尽管由于“计数到无穷大”问题（通过 15 跳限制缓解），在大拓扑中收敛可能很慢。
- **环路预防机制**：
  - **水平分割 (Split Horizon)**：不要将从某个接口学到的路由再经该接口通告回去。
  - **路由毒化 (Route Poisoning)**：使用度量标准 16（无穷大）通告失败的路由。
  - **毒性反转 (Poison Reverse)**：通过将毒化路由通告回源来覆盖水平分割。
  - **触发更新 (Triggered Updates)**：在拓扑发生变化时立即发送更新（在 RIPv2 中）。
  - **抑制计时器 (Hold-down Timers)**：在某个路由被标记为不可达后的一段时间内忽略该路由的更新。

### RIP 的版本
主要有三个版本：

1. **RIPv1** (RFC 1058, 1988)：
   - 有类路由（不发送子网掩码信息）。
   - 使用广播更新。
   - 无认证。
   - 不支持 VLSM (Variable Length Subnet Masking) 或 CIDR。

2. **RIPv2** (RFC 2453, 1998)：
   - 无类路由（更新中包含子网掩码）。
   - 使用多播 (224.0.0.9) 进行更新，减少网络开销。
   - 支持认证（明文或 MD5）。
   - 支持 VLSM、CIDR 和路由汇总。
   - 向后兼容 RIPv1。

3. **RIPng** (RIP Next Generation, RFC 2080)：
   - **IPv6** 的扩展。
   - 与 RIPv2 类似，但使用 UDP 端口 521 和多播组 FF02::9。
   - 支持 IPv6 地址（128 位）。
   - 保留 15 跳的跳数限制和其他机制。

### RIP 的优点
- 配置和理解简单。
- 广泛支持各种设备。
- 资源要求低。
- 自动在等价路径（最多 6 条路径）上进行负载均衡。

### 缺点和局限性
- 限制为 15 跳 → 不适合大型网络。
- 与 OSPF 等链路状态协议相比收敛缓慢。
- 带宽使用高（每 30 秒进行一次完整表更新）。
- 如果没有适当的措施，容易出现路由环路。
- RIPv1 缺乏安全性和现代功能。
- 在企业网络中已 largely 被 OSPF、EIGRP 或 IS-IS 取代。

由于其简单性，RIP 在小型网络、传统系统或教育目的中仍然有用。

参考文献：

- https://www.geeksforgeeks.org/computer-networks/routing-information-protocol-rip/
- https://en.wikipedia.org/wiki/Routing_Information_Protocol
- https://www.techtarget.com/searchnetworking/definition/Routing-Information-Protocol
- https://www.zenarmor.com/docs/network-basics/what-is-routing-information-protocol-rip
- https://www.juniper.net/documentation/us/en/software/junos/rip/topics/topic-map/rip-and-ripng-overview.html
