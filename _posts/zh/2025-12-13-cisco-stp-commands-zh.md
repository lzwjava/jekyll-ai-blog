---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cisco 生成树协议命令
translated: true
type: note
---

问题：Cisco 交换机上 Spanning Tree Protocol (STP) 的典型命令有哪些？

答案：

Spanning Tree Protocol (STP) 在 Cisco 交换机上默认启用，通常运行 Rapid Per-VLAN Spanning Tree (Rapid PVST+) 或 PVST+。典型命令分为两类：**验证/显示命令**（最常用于监控和故障排除）和**配置命令**（用于调整 STP 行为）。

### 验证/显示命令

这些是最常用的命令，用于检查 STP 状态、根桥、端口角色和拓扑。

- `show spanning-tree`
  显示所有 VLAN 的详细 STP 信息，包括根桥、端口角色（Root、Designated、Blocked）、开销和状态。

- `show spanning-tree vlan <vlan-id>`
  显示特定 VLAN 的 STP 详细信息（在存在许多 VLAN 时推荐使用，以避免冗长的输出）。

- `show spanning-tree summary`
  提供高级概述：STP 模式（例如 PVST、Rapid PVST+）、根状态、每个状态的端口计数以及已启用的功能，如 PortFast 或 Loopguard。

- `show spanning-tree detail`
  更详细的信息，包括计时器和端口信息。

- `show spanning-tree bridge`
  显示本地桥 ID 和计时器。

- `clear spanning-tree counters [interface]`
  清除 STP BPDU 计数器进行故障排除。

- `clear spanning-tree detected-protocols`
  强制 STP 协议迁移重新协商。

### 配置命令

在全局或接口配置模式下输入。STP 默认启用；这些命令用于调整它。

#### 全局配置

- `spanning-tree mode {rapid-pvst | pvst | mst | rstp | stp}`
  设置 STP 模式。Rapid PVST+ 在许多 Catalyst 交换机上是常见/默认设置，用于更快的收敛。

- `spanning-tree vlan <vlan-id> priority <value>`
  设置 VLAN 的桥优先级（4096 的倍数，值越低越有可能成为根）。默认值：32768。

- `spanning-tree vlan <vlan-id> root primary`
  自动设置低优先级，使该交换机成为根桥。

- `spanning-tree vlan <vlan-id> root secondary`
  使其成为辅助根。

- `spanning-tree hello-time <seconds>`
  设置 hello 间隔（默认值：2 秒）。

- `spanning-tree forward-time <seconds>`
  设置转发延迟（默认值：15 秒）。

- `spanning-tree max-age <seconds>`
  设置最大老化计时器（默认值：20 秒）。

#### 接口配置

- `spanning-tree portfast`
  启用 PortFast（在边缘端口上立即转发；用于连接主机的接入端口）。

- `spanning-tree bpduguard enable`
  如果端口收到 BPDU，则禁用该端口（防止意外环路）。

- `spanning-tree cost <value>`
  手动设置端口路径开销。

- `spanning-tree port-priority <value>`
  设置端口优先级（影响角色选择）。

- `spanning-tree guard root`
  启用根保护（防止劣质 BPDU 使端口成为根）。

- `spanning-tree link-type point-to-point`
  假定全双工点对点链路，以实现更快的 RSTP 收敛。

这些命令因交换机型号和 IOS 版本（例如，Catalyst 9200/9300 与旧的 2960）而略有不同。务必使用 `show running-config | include spanning-tree` 进行验证。

参考资料：

- [Cisco Catalyst Spanning Tree Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/software/release/16-12/configuration_guide/lyr2/b_1612_lyr2_9200_cg/configuring_spanning_tree_protocol.html)
- [Cisco Spanning Tree Protocol Guide with Examples](https://www.networkstraining.com/cisco-spanning-tree-protocol/)
- [Cisco CLI Guide for Spanning Tree Commands](https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1200-cli/spanning-tree-commands.html)
- [Cisco Press: Spanning Tree Configuration](https://www.ciscopress.com/articles/article.asp?p=2832407&seqNum=6)
