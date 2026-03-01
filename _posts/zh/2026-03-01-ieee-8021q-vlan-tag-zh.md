---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE 802.1Q VLAN 标签详解
translated: true
type: note
---

**问题**：根据 IEEE 802.1Q 标准，该标准定义了虚拟 LAN 环境中的 Ethernet 帧格式，使用一个 4-byte field 来指示发送帧的 host 所属的 virtual LAN。该字段的名称是什么？

**答案**：

正确答案是 **VLAN Tag**（或 **VLAN 标记** / **Tag**）。

在 IEEE 802.1Q 标准中，会在 Ethernet 帧中插入一个额外的 4-byte field，称为 **VLAN Tag**（也通常称为 802.1Q tag 或简称为“Tag”）。此 tag 用于标识帧所属的 Virtual Local Area Network (VLAN)。

VLAN Tag 的结构如下：

- **TPID** (Tag Protocol Identifier)：2 bytes，固定值 0x8100  
- **TCI** (Tag Control Information)：2 bytes，其中包含：  
  - Priority Code Point (PCP)：3 bits  
  - Drop Eligible Indicator (DEI)：1 bit（前身为 CFI）  
  - VLAN Identifier (VID)：12 bits（实际 VLAN 编号，0–4095）

这个 4-byte VLAN Tag field 使得交换机能够在同一物理链路（trunk link）上区分并分离来自不同 VLAN 的流量。

因此，用于指示发送 host 所属 VLAN 的 4-byte field 称为 **VLAN Tag**（或中文中的 VLAN 标记 / Tag）。

**参考文献**：  

- 无（基于 IEEE 802.1Q 规范的标准网络知识）