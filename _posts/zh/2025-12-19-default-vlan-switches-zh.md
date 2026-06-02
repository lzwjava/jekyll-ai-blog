---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 大多数交换机上的默认VLAN
translated: true
type: note
---

问题：大多数交换机上的默认 VLAN 是哪个？

答案：

正确答案是 **B) VLAN 1**。

在大多数网络交换机上（特别是 Cisco 交换机和许多遵循类似约定的其他供应商），VLAN 1 被配置为默认 VLAN。这意味着：

- 除非明确更改，否则所有交换机端口最初都分配给 VLAN 1。
- VLAN 1 通常用于管理流量（例如 Telnet、SSH、SNMP 或 CDP/LLDP）。
- 它也是 trunk 端口上的默认 native VLAN，这意味着未标记的帧与 VLAN 1 相关联。
- 最佳实践建议更改 native VLAN 并避免将 VLAN 1 用于常规数据流量，因为存在安全隐患（例如，潜在的 VLAN hopping 攻击）。

其他选项：

- **VLAN 0**：通常保留或不可用（通常用于内部目的，例如 blackholing traffic）。
- **VLAN 100**：不是默认值；属于扩展 VLAN 范围的一部分，用户可配置。
- **VLAN 1001**：通常在保留范围（Cisco 上 1002-1005 是传统 Token Ring/FDDI 的默认值），1001 不用作默认值。

这在 Cisco、Arista、Juniper（有一些变化）和其他大多数企业级交换机中都是标准配置。
