---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP/IP 协议层中的 IGMP
translated: true
type: note
---

**问题**：Internet Group Management Protocol (IGMP) 位于 TCP/IP 参考模型的哪一层？

**答案**：

Internet Group Management Protocol (IGMP) 位于 TCP/IP 参考模型的 **Network Layer**（也称为 **Internet Layer** 或 **Network Interconnection Layer**）。

### 解释：
1.  **IGMP 的功能**：IGMP 被 IP 网络上的主机和相邻路由器用于建立 multicast group memberships。它允许设备向附近的路由器报告其对特定 multicast group 数据包的兴趣。
2.  **在 TCP/IP 模型中的位置**：
    *   尽管 IGMP 消息被封装在 IP datagrams 中（类似于 TCP 或 UDP segments 的封装），但 IGMP 被视为 IP protocol suite 的组成部分。
    *   它与 IP 在同一逻辑层级运行，处理与 IP multicasting 相关的控制功能。
    *   因此，它被归类到 **Network Layer**（或 Internet Layer），该层负责逻辑寻址、路由和主机到主机的交付，包括 multicast management。
3.  **与 OSI 模型的比较**：在 OSI 模型中，IGMP 通常也与第 3 层（Network Layer）相关，尽管某些教科书可能松散地将它置于与 Data Link Layer 边界附近，因为它与本地网络硬件交互进行 multicast filtering。然而，在严格的 TCP/IP 模型上下文中，它属于与 IP、ICMP 和 ARP 一起的 Internet/Network layer protocols。

提供的参考答案“网络互联”（Network Interconnection）对应于 TCP/IP 模型中的 **Internet Layer**（网络层）。

**参考资料**：
- [RFC 1112 - Host extensions for IP multicasting](https://datatracker.ietf.org/doc/html/rfc1112)
- [Cloudflare - What is IGMP?](https://www.cloudflare.com/learning/network-layer/what-is-igmp/)
