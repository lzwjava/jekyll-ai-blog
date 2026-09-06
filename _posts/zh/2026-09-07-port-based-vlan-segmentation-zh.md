---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于端口的VLAN划分
translated: true
type: note
---

**问题：** 如何使用基于端口的方法分隔 VLAN 网络？

**回答：** 基于端口的 VLAN（也称为“接入端口”VLAN）是使用可管理交换机划分网络最常用的方式。每个物理交换机端口被分配至一个 VLAN，所有进入该端口的流量会自动打上对应 VLAN ID 的标签。不同 VLAN 中的设备必须通过路由器或三层交换机才能通信。

以下是其工作原理的示意图：

**逐步工作原理：**

**1. 将端口分配至 VLAN（接入端口）**
每个端口被配置为属于某个 VLAN 的 *接入端口*。任何插入的设备自动加入该 VLAN — 无需在设备上进行任何配置。

```
! Cisco IOS 示例
interface FastEthernet0/1
  switchport mode access
  switchport access vlan 10

interface FastEthernet0/4
  switchport mode access
  switchport access vlan 20
```

**2. 交换机隔离流量**
交换机在内部将入站帧打上 VLAN ID 标签。来自 VLAN 10 的帧*绝不会*被转发到 VLAN 20 或 VLAN 30 的端口 — 交换机在硬件层面强制执行此规则。

**3. 使用 Trunk 端口实现跨 VLAN 路由（如果需要）**
*Trunk 端口*将多个 VLAN 的带标签流量传输至路由器或三层交换机。路由器通过子接口（称为 *Router-on-a-Stick* 的技术）在 VLAN 之间进行路由，或者三层交换机在内部进行路由。

```
! Trunk 端口配置
interface FastEthernet0/8
  switchport mode trunk
  switchport trunk allowed vlan 10,20,30
```

**需要记住的关键规则：**

- 处于*同一* VLAN 中的设备可以通过交换机自由通信（二层）。
- 处于*不同* VLAN 中的设备被隔离 — 通信需要路由器或三层交换机。
- 端口分配是按每个交换机端口进行的，而非按设备，因此设备继承其插入端口的 VLAN。
- Trunk 端口是唯一的例外 —— 它们使用 802.1Q 标签同时承载多个 VLAN。

---

**参考资料：**

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/vlan/b_1612_vlan_9300_cg/configuring_vlans.html)
- [IEEE 802.1Q VLAN Standard Overview](https://www.ieee802.org/1/pages/802.1Q.html)
- [Port-Based VLAN — NetworkLessons.com](https://networklessons.com/switching/introduction-to-vlans)
