---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 交换与路由考试知识点
translated: true
type: note
---

以下是根据教学大纲项目和考核目标整理的《交换与路由技术》(13833) 考试 100 个知识点详单。

### 项目 1：eNSP 与 VRP 基础

1. **eNSP 用途：** eNSP 是一款图形化网络仿真平台，用于模拟 Huawei 企业级网络设备。
2. **VRP 系统：** Versatile Routing Platform (VRP) 是 Huawei 网络设备使用的操作系统。
3. **用户视图 (User View)：** 登录后的初始视图，以 `<Huawei>` 表示，用于查看设备基本信息。
4. **系统视图 (System View)：** 使用 `system-view` 命令进入，用于修改全局设备参数。
5. **接口视图 (Interface View)：** 用于配置特定的物理或逻辑端口（例：`interface GigabitEthernet 0/0/1`）。
6. **命令补全：** 使用 Tab 键自动补全未输入完整的命令。
7. **问号 (?)：** 提供可用命令列表或命令参数帮助。
8. **保存配置：** `save` 命令将当前配置存储在 flash 中，防止重启后数据丢失。
9. **Undo 命令：** `undo` 关键字用于删除配置或禁用特定功能。
10. **查看命令：** `display` 命令（如 `display this`）用于查看当前状态或配置设置。

---

### 项目 2：交换技术与园区网络

11. **二层交换 (Layer 2 Switching)：** 交换机在 Data Link Layer 根据 Destination MAC 地址转发数据帧。
12. **MAC 地址表：** 记录 MAC 地址与交换机物理端口对应关系的动态表。
13. **三层交换 (Layer 3 Switching)：** 结合了二层交换与三层路由技术，实现 VLAN 间的高速数据转发。
14. **VLAN 定义：** Virtual Local Area Networks 将物理网络逻辑划分为多个广播域。
15. **VLAN 优点：** 增强安全性、减少广播流量、简化网络管理。
16. **Access 端口：** 用于连接终端设备（如 PC）的端口类型，属于单个 VLAN。
17. **Trunk 端口：** 允许在交换机之间的单条物理链路上传输多个 VLAN 流量的端口类型。
18. **Hybrid 端口：** Huawei 特有的端口类型，可灵活处理 tagged 和 untagged 流量。
19. **PVID：** Port VLAN ID 标识进入端口的 untagged 数据帧所属的默认 VLAN。
20. **IEEE 802.1Q：** 以太网帧中 VLAN tagging 的标准行业协议。
21. **VLAN 间路由：** 通过三层交换机或路由器实现不同 VLAN 间的通信。
22. **VLANIF 接口：** 交换机上的逻辑三层接口，用作特定 VLAN 的网关。
23. **链路聚合 (Link Aggregation)：** 将多个物理链路组合成一个逻辑链路，以增加带宽并提供冗余。
24. **LACP 协议：** Link Aggregation Control Protocol 用于动态协商和管理聚合链路。
25. **网络环路：** 当交换机之间存在多条活动路径时产生，会导致广播风暴。
26. **STP (Spanning Tree Protocol)：** 通过逻辑阻塞冗余端口来防止网络环路。
27. **根桥 (Root Bridge)：** STP 拓扑中的中心交换机，根据最低的 Bridge ID 选出。
28. **RSTP (Rapid STP)：** STP 的演进版本，在拓扑变化时提供更快的收敛速度。
29. **VRRP (Virtual Router Redundancy Protocol)：** 通过将多个路由器/交换机分组为一个虚拟路由器来提供网关冗余。
30. **Master 路由器：** VRRP 组中的活动设备，负责转发流量。
31. **Backup 路由器：** VRRP 组中的备用设备，在 Master 故障时接管工作。
32. **DHCP (Dynamic Host Configuration Protocol)：** 自动为网络主机分配 IP 地址、掩码和网关。
33. **DHCP 服务器：** 管理 IP 地址池并出租地址的设备（路由器或交换机）。
34. **DHCP 中继 (DHCP Relay)：** 允许 DHCP 服务器为位于不同子网/VLAN 的客户端提供地址。
35. **Console 端口：** 用于交换机或路由器本地初始化配置的物理管理端口。
36. **Telnet/SSH：** 用于通过网络远程管理网络设备的协议。
37. **全双工 (Full-Duplex)：** 允许交换机端口同时进行双向数据传输。
38. **半双工 (Half-Duplex)：** 允许双向数据传输，但同一时刻只能有一个方向。
39. **端口安全 (Port Security)：** 限制单个交换机端口允许学习的 MAC 地址数量的功能。
40. **广播风暴：** 过多的广播流量消耗所有带宽并导致网络瘫痪。

---

### 项目 3：路由技术与互联网络

41. **路由器功能：** 连接不同网段并确定 IP 包转发的最佳路径。
42. **路由表：** 路由器中存储通往各个网络目的地路径的数据库。
43. **直连路由 (Directly Connected Route)：** 当路由器接口配置 IP 且状态为 active 时自动创建。
44. **静态路由 (Static Route)：** 由管理员手动配置的通往目的网络的路径。
45. **默认路由 (Default Route)：** 一种特殊的静态路由 (0.0.0.0/0)，用于在路由表中找不到匹配项时使用。
46. **浮动静态路由：** 具有更高优先级值的备份静态路由，仅在主链路失效时出现。
47. **动态路由：** 允许路由器自动学习并共享网络拓扑变化的协议。
48. **度量值 (Metric)：** 路由协议用于衡量特定路径“开销”或效率的数值。
49. **管理距离/优先级 (Administrative Distance/Preference)：** 当多个协议提供相同目的地时，用于选择最佳路由的数值。
50. **RIP (Routing Information Protocol)：** 一种使用“跳数 (hop count)”作为度量值的距离矢量协议。
51. **RIPv2：** RIP 的更新版本，支持 VLSM 并使用组播 (224.0.0.9) 进行更新。
52. **OSPF (Open Shortest Path First)：** 一种使用 Shortest Path First (SPF) 算法的链路状态协议。
53. **OSPF 区域 (Area)：** OSPF 路由器的逻辑分组，用于限制 Link-State Database 的大小。
54. **OSPF 区域 0：** OSPF 网络中的骨干区域，所有其他区域必须与之相连。
55. **Router ID：** 在 OSPF 进程中用于唯一标识路由器的 32 位数字。
56. **邻居关系 (Neighbor Relationship)：** 两个 OSPF 路由器交换 Hello 包并就参数达成一致的状态。
57. **邻接关系 (Adjacency)：** OSPF 邻居同步其 Link-State Database 的更高级状态。
58. **单臂路由 (One-Arm Routing)：** 在路由器上使用单个物理接口（配置子接口）在多个 VLAN 间进行路由。
59. **子接口 (Sub-interface)：** 物理接口的逻辑划分，用于 Router-on-a-Stick 配置。
60. **Dot1q 终结：** 路由器子接口剥离 VLAN 标签以处理 IP 包的过程。
61. **NAT (Network Address Translation)：** 将私有内部 IP 地址转换为公有 IP 地址以访问 Internet。
62. **静态 NAT：** 私有 IP 与公有 IP 地址之间的一对一映射。
63. **动态 NAT：** 将私有 IP 映射到公有 IP 地址池，采用先到先得原则。
64. **NAPT (Network Address Port Translation)：** 允许通过使用不同端口号让多个内部主机共享一个公有 IP。
65. **ACL (Access Control List)：** 根据 IP 地址或端口号允许或拒绝流量的一系列规则。
66. **基本 ACL：** 使用范围 2000-2999，仅根据源 IP 地址进行过滤。
67. **高级 ACL：** 使用范围 3000-3999，根据源/目的 IP、协议和端口号进行过滤。
68. **ACL 规则 "Deny"：** 明确丢弃匹配规则中指定条件的报文。
69. **ACL 规则 "Permit"：** 允许匹配指定条件的报文通过。
70. **通配符掩码 (Wildcard Mask)：** 在 ACL 中用于指定 IP 地址中哪些位在匹配时应被忽略。
71. **PPP (Point-to-Point Protocol)：** 广泛用于两个路由器之间直接连接的 Data Link Layer 协议。
72. **CHAP 认证：** PPP 链路中使用的一种安全的三次握手认证方法。
73. **IPv6 地址：** 旨在取代 IPv4 的 128 位地址，以八组十六进制数字编写。
74. **IPv6 无状态自动配置 (SLAAC)：** 允许主机利用路由器提供的 Prefix 自动生成自己的 IPv6 地址。
75. **双栈 (Dual Stack)：** 在同一网络设备上同时运行 IPv4 和 IPv6。
76. **路由重分发 (Route Redistribution)：** 允许路由器将从一种协议学到的路由共享到另一种协议（如 RIP 到 OSPF）的过程。
77. **收敛 (Convergence)：** 网络发生变化后，所有路由器更新其路由表所需的时间。
78. **水平分割 (Split Horizon)：** RIP 用于防止路由环路的技术，规定不将路由信息发回学到该信息的接口。
79. **LSA (Link State Advertisement)：** OSPF 用于与邻居共享本地拓扑信息的数据包。
80. **DR (Designated Router)：** OSPF 多路访问网段中的指定路由器，负责管理 LSA。

---

### 项目 4：高级配置与设计

81. **子网划分 (Subnetting)：** 将一个大网络划分为多个更小、更易管理的子网络的过程。
82. **CIDR (Classless Inter-Domain Routing)：** 取代传统的 A、B、C 类分类的 IP 编址方法。
83. **子网掩码：** 区分 IP 地址的网络部分与主机部分的 32 位数字。
84. **网关 (Gateway)：** 本地网络通往其他网络的出口点，通常是路由器或三层交换机。
85. **Loopback 接口：** 路由器上的虚拟接口，用于测试及作为 OSPF 的稳定标识符。
86. **ARP (Address Resolution Protocol)：** 将已知的 IP 地址解析为物理 MAC 地址。
87. **代理 ARP (Proxy ARP)：** 允许路由器代答其可达但未直接连接网络的 ARP 请求。
88. **Tracert：** 一种诊断工具，用于追踪数据包到达目的地经过的逐跳路径。
89. **Ping：** 使用 ICMP Echo 消息测试两个 IP 设备之间的基本连通性。
90. **带宽 (Bandwidth)：** 网络中给定路径的最大数据传输速率。
91. **吞吐量 (Throughput)：** 在特定时间内成功传送数据的实际速率。
92. **VLAN 修剪 (VLAN Pruning)：** 限制 Trunk 链路上的 VLAN 流量，仅允许发送至在该 VLAN 中有活动成员的交换机。
93. **根端口 (Root Port)：** 非根桥上通往 Root Bridge 路径开销最低的端口。
94. **指定端口 (Designated Port)：** 网络段上负责转发 STP 流量的端口。
95. **MTU (Maximum Transmission Unit)：** 网络接口能传输的最大数据单元大小。
96. **冷启动 (Cold Boot)：** 从断电状态启动设备。
97. **热启动/重启 (Warm Boot/Reboot)：** 在不断电的情况下重新启动设备，通常用于应用新配置。
98. **网络拓扑：** 网络的物理或逻辑布局（如星型、网状、总线型）。
99. **标准化：** 使用 OSPF 和 STP 等协议以确保不同厂商设备之间的兼容性。
100. **排错 (Troubleshooting)：** 识别、定位并修复网络配置中故障的系统化过程。