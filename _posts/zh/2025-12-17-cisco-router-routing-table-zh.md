---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cisco 路由器路由表命令
translated: true
type: note
---

问题：哪个命令显示Cisco路由器上的路由表，为什么D是正确答案？

答案：

正确答案是 **A) show ip route**。

### 全面解释

- **show ip route**：这是Cisco IOS中用于显示路由器上IP路由表的主要命令。路由表包含有关已知网络（目的地）、它们的学习方式（例如，直连、静态或通过OSPF、EIGRP、RIP、BGP等动态路由协议）、下一跳地址、管理距离、度量、以及出站接口的信息。它对于排除路由问题、验证路由安装以及了解路由器如何转发数据包至关重要。

  输出示例片段：

  ```
  Router# show ip route
  Codes: C - connected, S - static, R - RIP, O - OSPF, B - BGP ...
  Gateway of last resort is 203.0.113.1 to network 0.0.0.0

  C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
  O    10.0.0.0/8 [110/20] via 172.16.1.2, GigabitEthernet0/1
  S*   0.0.0.0/0 [1/0] via 203.0.113.1
  ```

- **show interfaces**：此命令显示所有路由器接口（或指定接口，例如 `show interfaces GigabitEthernet0/0`）的详细状态和统计信息。它包括在线/离线状态、IP地址、MTU、带宽、错误和流量计数器等信息。它**不**显示路由表。

- **show vlan**：此命令主要用于Cisco交换机（而非路由器）来显示VLAN配置和成员信息。在多层交换机上，它可能会显示与VLAN相关的详细信息，但与路由器上的IP路由表无关。

- **show mac address-table**：此命令用于Cisco交换机，显示MAC地址表（CAM表），其中显示已学习的MAC地址、相关端口和VLAN。它与IP路由无关，并且在纯路由器上不存在或功能不同。

### 为什么用户选择D是错误的

选择 **D) show mac address-table** 表明可能混淆了第2层交换功能（交换机上的MAC学习和转发）和第3层路由功能（路由器上的IP路由查找）。路由器主要在第3层运行，并维护一个路由表用于IP转发决策，而MAC地址表是交换机使用的第2层构造。

总而言之，要在Cisco路由器上查看路由表，应始终使用 **show ip route**（或其变体，如 `show ip route ospf` 以按协议过滤）。
