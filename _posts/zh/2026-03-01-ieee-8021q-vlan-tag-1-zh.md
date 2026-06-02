---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE 802.1Q VLAN 标签结构详解
translated: true
type: note
---

问题：提供 IEEE 802.1Q 标准中定义的 VLAN Tag 结构的详细扩展和解释，包括 TPID 和 TCI 字段及其子组件。

答案：

**VLAN Tag**（也称为 802.1Q tag）是一个 4 字节（32 位）字段，它被插入到 Ethernet 帧中以支持 Virtual LANs (VLANs)，如 IEEE 802.1Q 标准所定义。它位于原始 Ethernet II 帧的 Source MAC Address 和 EtherType/Length 字段之间。

VLAN Tag 的完整结构如下：

- **TPID – Tag Protocol Identifier**（16 位 / 2 字节）
  - 固定值：**0x8100**
  - 此值标识帧为 IEEE 802.1Q 标记帧。
  - 当交换机或其他设备看到 EtherType = 0x8100 时，它知道接下来的 2 字节包含 VLAN 相关控制信息，而真正的 EtherType 在其后跟随。

- **TCI – Tag Control Information**（16 位 / 2 字节）
  TCI 字段进一步分为三个子字段：

  1. **PCP – Priority Code Point**（3 位）
     - 也称为 Class of Service (CoS) 字段。
     - 值范围为 0 到 7。
     - 用于指示帧的优先级（Quality of Service – QoS）。
     - 较高值通常表示较高优先级（例如，7 = 网络控制流量，5 = 语音，0 = 尽力而为）。
     - 这允许交换机根据优先级应用不同的排队和转发行为。

  2. **DEI – Drop Eligible Indicator**（1 位）
     - 在早期版本中称为 **CFI**（Canonical Format Indicator）。
     - 在现代用法（IEEE 802.1Q 修正后），它是 **Drop Eligible Indicator**。
     - 0 = 帧不可丢弃（优先流量）
     - 1 = 帧可丢弃（拥塞时优先丢弃）
     - 此位特别适用于 PCP 值映射到支持丢弃优先级的服务类（类似于 IP DiffServ 的 ECN 或 ATM CLP 位）。

  3. **VID – VLAN Identifier**（12 位）
     - 实际的 VLAN 编号。
     - 范围：0 到 4095（2¹² = 4096 个可能值）。
     - 常用值：
       - 0 = 保留（有时用于无 VLAN 的优先级标记帧）
       - 1 = 默认 VLAN（通常在 trunk 上称为 native VLAN）
       - 2–4094 = 用户可分配 VLAN ID
       - 4095 = 保留
     - VID 是确定帧所属 VLAN 的主要字段。

32 位 VLAN Tag 的完整位布局：

```
Bits:    15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
         ┌──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┐  ← TPID (16 bits)
         │                 0x8100 (fixed)                 │
         └─────────────────────────────────────────────────┘
Bits:    15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
         ┌───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┐  ← TCI (16 bits)
         │ PCP     │ DEI │          VID (12 bits)         │
         └─────────┴─────┴─────────────────────────────────┘
```

总计：4 字节 = 32 位 = TPID（16 位） + TCI（16 位）。

此标记启用：
- 在单个物理链路上进行 VLAN 分段（trunking）
- Quality of Service 差异化
- 拥塞期间的选择性丢弃

参考文献：

- 无（基于 IEEE 802.1Q 规范的标准知识）
