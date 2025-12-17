---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换与路由技术发展史
translated: true
type: note
---

问题：交换和路由技术的历史是什么？

答案：

### 概述
交换和路由技术构成了现代计算机网络的基础，用于实现设备之间的数据传输。交换主要在OSI模型的第2层（数据链路层）操作，侧重于局域网（例如以太网LAN），而路由在第3层（网络层）工作，处理网络之间的互连（例如互联网）。其演变从电路交换（专用路径，如传统电话）转向分组交换（数据分成数据包进行高效共享传输）。

### 早期基础：电路交换与分组交换
- **电路交换**：起源于19世纪后期，与模拟电话网络（例如亚历山大·格雷厄姆·贝尔在1878年的系统）一起出现。它为整个通信会话建立一条专用的物理路径，确保恒定带宽和低延迟，但在空闲期间会浪费资源。
- **分组交换**：在20世纪60年代初期作为数据网络更高效的替代方案独立发明。
  - 保罗·巴兰（RAND Corporation，美国）在1960年至1964年提出了“分布式自适应消息块交换”，用于可生存的军事网络。
  - 唐纳德·戴维斯（英国）在1965年至1966年创造了“分组交换”一词。
  - 这种方法将数据分解成数据包，每个数据包独立路由，实现带宽共享和更好的资源利用。

分组交换因其灵活性、容错性和效率而成为数据网络的主流。

### 分组交换和早期网络的关键里程碑
- **1969年**：ARPANET（互联网的前身）上发送了第一个分组交换消息，使用Interface Message Processors (IMPs) 作为早期的路由器/交换机。ARPANET连接了四个节点并展示了分组交换。
- **20世纪70年代**：ARPANET扩展；早期路由器得到开发（例如施乐PARC在1974年）。TCP/IP等协议出现（Vint Cerf和Bob Kahn，1974年）。
- **1983年**：ARPANET完全过渡到TCP/IP，标志着现代互联网的诞生。

### 交换技术的演变
- **20世纪80年代前**：网络使用集线器/网桥（共享介质，广播流量，容易发生冲突）。
- **1983年**：Mark Kempf 在Digital Equipment Corporation (DEC) 公司发明了第一个以太网网桥。
- **1990年**：Kalpana推出第一个商用以太网交换机，实现每个端口的专用带宽并减少冲突。
- **20世纪90年代至21世纪初期**：Layer 2 交换机主导局域网；引入VLANs、Spanning Tree Protocol (STP) 用于环路预防。
- **21世纪初至今**：多层交换机（Layer 3 switching）整合路由功能；可编程交换机和SDN (Software-Defined Networking) 允许动态控制。

### 路由技术的演变
- **1969年至20世纪80年代**：早期的距离矢量协议，如RIP (Routing Information Protocol，1988年正式化，但根源于1969年的ARPANET)。
- **20世纪80年代**：开发了链路状态协议（例如IS-IS）和外部网关（EGP，1984年）。
- **20世纪90年代**：OSPF (Open Shortest Path First) 和BGP (Border Gateway Protocol，1995年发布版本4) 用于可扩展的互联网路由；RIPv2增加了无类别路由。
- **21世纪初至今**：针对IPv6、MPLS (Multiprotocol Label Switching)、ECMP (Equal-Cost Multi-Path) 的增强，以及与SDN/NFV的集成。现代路由器使用ASICs进行高速转发。

### 现代发展
如今，交换和路由在多层交换机等设备中融合。趋势包括虚拟化、云集成、安全功能（例如防火墙）以及对高带宽应用（5G、IoT）的支持。分组交换驱动着全球互联网，并在效率、安全性和可扩展性方面不断改进。

参考文献：  

- [Packet switching - Wikipedia](https://en.wikipedia.org/wiki/Packet_switching)
- [Packet Switching - Engineering and Technology History Wiki](https://ethw.org/Packet_Switching)
- [Network switch - Wikipedia](https://en.wikipedia.org/wiki/Network_switch)
- [Router (computing) - Wikipedia](https://en.wikipedia.org/wiki/Router_%28computing%29)
- [The history of network switching](https://silvanogai.github.io/posts/history/)
- [Network switches: past, present and future](https://news.networktigers.com/all-articles/network-switches-past-present-and-future/)