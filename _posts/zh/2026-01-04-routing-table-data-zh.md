---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 路由表结构和存储数据
translated: true
type: note
---

Question: Routing table 的外观是什么样的，其中需要存储哪些信息？具体来说，它是否包含 MAC addresses、IP addresses 以及有关如何进行 packet routing 的信息？

Answer: 

**Routing table**（路由表）是由 router（以及支持 IP 的 host）维护的数据结构，用于根据目标 IP address 决定将 IP packets 转发到何处。

### Routing Table 的典型外观
在大多数系统上，可以使用如下命令显示 routing table：

- Linux/macOS: `ip route show` 或 `route -n`
- Windows: `route print`

一个（来自 Linux 系统的）示例 routing table 可能如下所示：

```
default via 192.168.1.1 dev eth0 proto dhcp metric 100 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 metric 100 
10.0.0.0/24 via 10.0.0.254 dev tun0 
172.16.0.0/16 via 192.168.1.50 dev eth0
```

或者采用传统的 `netstat -rn` / `route` 格式：

```
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0
10.0.0.0        10.0.0.254      255.255.255.0   UG    0      0        0 tun0
```

### Routing Table 每个条目中存储的关键信息
routing table 中的每个条目通常包含以下字段：

- **Destination network/prefix**: 此路由适用的网络或主机 IP address 范围（例如 192.168.1.0/24 或用于默认路由的 0.0.0.0/0）。
- **Prefix length / Netmask**: 定义目标网络的规模（例如 /24 或 255.255.255.0）。
- **Gateway / Next hop**: 如果目的地不是直接连接的，则为转发 packet 的下一个 router 的 IP address。如果 gateway 为 0.0.0.0 或不存在，则表示该网络是直接连接的。
- **Interface / Output interface**: 发送 packet 所通过的本地网络接口（例如 eth0, wlan0, tun0）。
- **Metric / Administrative distance**: 当同一目的地存在多条路由时，用于优先选择某条路由的值（越小越好）。
- **Protocol / Source**: 路由是如何学习到的（static, kernel, DHCP, RIP, OSPF, BGP 等）。
- **Flags**: 标识符，如 U (up/可用), G (gateway), H (host route), D (dynamic) 等。

### Routing Table 是否包含 MAC Addresses？
**不包含。**  
Routing tables 运行在 OSI 模型的 **Layer 3 (IP layer)**，**不**存储 MAC addresses。MAC addresses 属于 Layer 2 (data link layer) 信息，由 **ARP table** (Address Resolution Protocol cache) 单独处理。

- Routing table 决定使用 **哪一个 next-hop IP address** 或 **哪一个 interface**。
- 一旦确定了 next-hop IP，如果 packet 必须通过本地链路（Ethernet, Wi-Fi 等）发送，系统会查询 **ARP table** 将 next-hop IP 解析为 MAC address，以便封装 Ethernet packet。

### Routing Table 是否包含 IP Addresses？
**是的。**  
- Destination network (IP prefix)
- Next-hop IP address (gateway)
- 有时还包括用于该接口的 source IP

### 它是否告知“哪个 Packet 路由到哪里”？
**是的。**  
Routing table 的主要目的正是如此：对于 packet 中给定的目标 IP address，对目标条目执行 **longest-prefix match**（最长前缀匹配）以决定：
- 是将 packet 转发给特定的 next-hop router (gateway IP)，还是
- 直接从本地 interface 发出（如果目的地在直接连接的网络上）。

总结：

| 信息 | 是否存在于 Routing Table 中？ | 备注 |
|------------------------------|---------------------------|-------|
| Destination IP network/prefix| 是 | 核心字段 |
| Netmask / Prefix length | 是 | 定义网络规模 |
| Next-hop / Gateway IP | 是 (如果不是直连) | 下一个 router 的 IP address |
| Output interface | 是 | 要使用的本地接口 |
| Metric / Priority | 是 | 用于路由选择 |
| MAC addresses | 否 | 由 ARP table 处理 (Layer 2) |
| Source IP (有时) | 是 | 用于 policy-based routing 或接口分配 |

References:  

- [Cisco: Understanding Routing Tables](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13762-40.html)
- [Linux ip-route man page](https://man7.org/linux/man-pages/man8/ip-route.8.html)
- [Microsoft: Route Command Reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/route_ws2008)