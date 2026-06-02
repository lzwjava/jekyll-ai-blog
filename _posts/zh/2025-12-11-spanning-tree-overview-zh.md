---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 生成树协议概述
translated: true
type: note
---

问题：什么是生成树协议 (STP)？您能提供一个全面的介绍吗？

答案：

生成树协议 (STP) 是一种在 IEEE 802.1D 中定义的第 2 层网络协议，用于防止通过冗余链路构建的以太网网络中出现环路。环路非常危险，因为它们会导致广播风暴、MAC 地址表不稳定，并可能在几秒钟内使整个交换网络瘫痪。STP 通过在保持完全连接的同时自动禁用冗余路径来解决此问题，从而创建一个逻辑上无环路的树形拓扑，该拓扑“跨越”网络中的所有交换机。

### 关键概念和目标
- 目标：确保第 2 层域中任意两个节点之间只有一条逻辑路径，同时允许物理冗余以实现容错。
- 当链路或交换机发生故障时，STP 会自动重新配置拓扑（收敛）以使用以前被阻塞的路径。
- 对终端设备（PC、服务器等）透明操作——它们只看到一条活动路径。

### STP 的核心组件（原始 802.1D）
1. **Bridge ID (BID)**
   8 字节：2 字节 Bridge Priority（默认 32768）+ 6 字节 MAC 地址。
   BID 越低，成为 Root Bridge 的可能性越大。

2. **Root Bridge**
   整个生成树拓扑的“参考点”。
   所有其他交换机都计算其通往 Root 的最佳路径。
   每个网络（或在后续版本中每个 VLAN）只有一个 Root Bridge。

3. **Path Cost**
   遍历链路的成本，基于带宽（IEEE 802.1D-1998 值）：
   - 10 Mbps → 100
   - 100 Mbps → 19
   - 1 Gbps → 4
   - 10 Gbps → 2
   （802.1t 中的现代“短模式”使用较小的数字：1G = 20 000，10G = 2 000 等）

4. **Port Roles**
   - Root Port (RP)：每个非根交换机上通往 Root Bridge 的最佳路径（最低累计路径成本）。每个交换机只有一个（Root 除外）。
   - Designated Port (DP)：每个 LAN 网段上向 Root 转发流量的端口。每个网段只有一个。
   - Blocked Port (Alternate/Backup)：所有其他端口——它们侦听但不转发任何流量（防止环路）。

5. **Port States**（原始 802.1D – 收敛非常慢）
   - Blocking → Listening → Learning → Forwarding（总共 20-50 秒）
   - Disabled

### STP 选举和操作过程
1. 每个交换机最初都认为自己是 Root，并每 2 秒（Hello Time）从所有端口发送 Bridge Protocol Data Units (BPDUs)。
2. 当交换机收到一个更“优”的 BPDU（更低的 Root BID，或相同的 Root 但更低的成本/发送者 BID/端口优先级）时，它停止声明自己是 Root，并开始转发该更“优”的 BPDU。
3. Root Bridge 选举：最低的 BID 获胜。决胜局是最低的 MAC 地址。
4. 每个非根交换机选择：
   - 一个 Root Port（到 Root 的最低成本路径）
   - 它连接到的每个网段的 Designated Ports
   - 所有剩余端口变为 Blocked
5. 拓扑变化通知 (TCN) 过程通知 Root，然后 Root 缩短 MAC 地址老化时间以实现更快恢复。

### 多年来的主要改进

| 版本                  | 年份 | 关键功能                                                                 | 收敛时间 |
|--------------------------|------|------------------------------------------------------------------------------|------------------|
| 原始 STP (802.1D)    | 1990 → 1998 | 基本环路预防，慢速端口状态                                       | 30-50 秒    |
| Rapid STP (RSTP, 802.1w) | 2001 | Alternate/Backup 端口，提议/协议，快速转换                  | < 1-3 秒    |
| Per-VLAN STP (PVST/PVST+) | Cisco | 每个 VLAN 一个 STP 实例                                                    | 与基础 STP 相同     |
| Rapid PVST+              | Cisco | 每个 VLAN 的 RSTP                                                                | 亚秒级       |
| Multiple STP (MSTP, 802.1s)| 2002 | 将多个 VLAN 映射到少数实例，可与 RSTP 互操作                     | 亚秒级       |

### RSTP (802.1w) 的主要增强功能
- 只有三种端口状态：Discarding、Learning、Forwarding（Blocking+Listening+Disabled 合并为 Discarding）
- 拓扑变化时端口可以立即转换
- 用于即时 Designated 端口激活的 Proposal/Agreement 握手
- 明确定义了 Backup 和 Alternate 端口角色
- 集成了 UplinkFast、BackboneFast 和 PortFast 功能

### 常见的扩展和功能（主要是 Cisco）
- PortFast – 立即将接入端口置于 Forwarding 状态（针对终端设备）
- BPDU Guard – 关闭收到 BPDU 的 PortFast 端口（防止流氓交换机）
- BPDU Filter – 停止发送/接收 BPDU（很少使用）
- Root Guard – 如果收到更“优”的 BPDU，阻止端口成为 Root Port
- Loop Guard – 如果 BPDU 停止到达，阻止端口进入 Forwarding 状态

### 示例拓扑（简单）

```
         [SW1 - Root]
        /    1G    \
   1G /            \ 1G
[SW2]              [SW3]
   \                /
    \   100M       /
     [SW4]------[SW5]
```

SW1 将成为 Root（假设 BID 最低）。
SW2 和 SW3 连接到 SW1 的端口将是 Root Port。
SW2-SW4-SW5-SW3 链路将具有最高成本路径，因此该网段上的一个端口（可能在 SW4 或 SW5 上）将被阻塞。

### STP 计时器汇总表（默认）

| 计时器             | 默认值 | 含义                                      |
|-------------------|---------------|----------------------------------------------|
| Hello Time        | 2 秒     | BPDU 传输间隔                   |
| Forward Delay     | 15 秒    | 处于 Listening + Learning 状态的时间（传统）  |
| Max Age           | 20 秒    | 在超时之前保留旧 BPDU 信息的时间 |
| Message Age       | 递增    | 收到 BPDU 中的 Age 字段                  |

在现代网络中，几乎所有人都使用 Rapid STP (802.1w) 或其 Cisco 变体（Rapid PVST+、MSTP），因为经典 STP 在发生故障后收敛时间太长。

STP 是以太网网络中第 2 层冗余的基础。即使有更新的技术（TRILL、SPB、带有 EVPN 的 VXLAN），理解经典和快速 STP 对任何网络工程师来说仍然至关重要。

参考文献：
- IEEE 802.1D-2004 Standard
- IEEE 802.1w-2001 (Rapid Spanning Tree Protocol)
- IEEE 802.1Q-2018 (includes MSTP)
- Cisco Press – “CCNP SWITCH 300-115 Official Cert Guide” (Chapters on STP)
