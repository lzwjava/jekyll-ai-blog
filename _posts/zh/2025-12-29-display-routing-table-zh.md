---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 显示路由表命令
translated: true
type: note
---

Question: Which command displays the routing table on a router?

Answer:

The correct answer is **A) show ip route**。

This command 用于在 Cisco routers（以及许多运行 Cisco IOS 或类似 operating systems 的设备）上显示当前的 IP routing table。routing table 包含有关已获知的 networks、next-hop addresses、metrics 以及 routing information 来源（例如 connected、static 或 OSPF、BGP 等 dynamic protocols）的信息。

### Explanation of options:

- **A) show ip route** – 正确。直接显示 IPv4 routing table。
- **B) show interfaces** – 显示 physical 和 logical interfaces 的 status 和 statistics（例如 up/down 状态、IP addresses、errors），但不显示 routing table。
- **C) show vlan** – 显示 switches 上的 VLAN configuration 和 status，与 router 上的 routing table 无关。
- **D) show mac address-table** – 显示 switches 上的 Layer 2 MAC address table (CAM table)，用于 VLAN 内的 frame forwarding，而非 routing。

这个问题通常出现在 CCNA 等 Cisco certification exams 中，掌握基础的 show commands 是至关重要的。
