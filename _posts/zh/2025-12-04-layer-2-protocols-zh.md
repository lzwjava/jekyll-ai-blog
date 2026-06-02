---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 第二层协议与技术
translated: true
type: note
---

问题：OSI 模型的第 2 层（数据链路层）通常运行哪些事物/协议？

回答：

**数据链路层（第 2 层）**负责通过物理链路进行帧的节点到节点传输、错误检测/纠正和介质访问控制。以下协议、技术和功能通常在第 2 层运行：

### 常见的第 2 层协议

- **Ethernet** (IEEE 802.3) – 最广泛使用的 LAN 技术
- **Wi-Fi** (IEEE 802.11) – 无线 LAN 帧和介质访问
- **PPP** (Point-to-Point Protocol) – 用于串行链路（例如，WAN、拨号）
- **HDLC** (High-Level Data Link Control) – 串行链路协议
- **Frame Relay** – 传统 WAN 技术
- **ATM** (Asynchronous Transfer Mode) – 基于单元的第 2 层协议
- **MPLS** (Multiprotocol Label Switching) – 通常被认为是 2.5 层，但在第 2 层插入标签
- **LLDP** (Link Layer Discovery Protocol) – 邻居发现（Cisco 使用 CDP 代替）
- **STP** (Spanning Tree Protocol) 及其变体 (RSTP, MSTP) – 防止第 2 层环路
- **LACP** (Link Aggregation Control Protocol, 802.1AX/802.3ad 的一部分) – EtherChannel/端口通道协商
- **ARP** (Address Resolution Protocol) – 技术上在第 2 层和第 3 层之间运行（将 IP 解析为 MAC），但使用第 2 层帧

### 第 2 层技术和概念

- **MAC addresses** (48 位硬件地址)
- **Switches** 和 **bridges** – 主要的第 2 层设备
- **VLANs** (802.1Q tagging)
- **MAC address table** (CAM table) 学习和转发
- **Frame encapsulation** (Ethernet frames, Wi-Fi frames 等)
- **Error detection** (通过 FCS – Frame Check Sequence 使用 CRC)
- **Flow control** (例如，Ethernet pause frames)

### 总结表

| 类别              | 示例                                      |
|-------------------|-------------------------------------------|
| 有线 LAN          | Ethernet (802.3)                          |
| 无线 LAN          | Wi-Fi (802.11)                            |
| WAN/串行          | PPP, HDLC, Frame Relay                    |
| 交换协议          | STP, RSTP, LACP, LLDP/CDP                 |
| VLAN 标记         | 802.1Q                                    |
| 地址寻址          | MAC addresses, ARP                        |

简而言之：**任何涉及 MAC 地址、帧（而非数据包）、交换机和物理链路特定帧的事物都属于第 2 层。**
第 3 层（例如，IP、ICMP、路由协议）在这些第 2 层协议之上，在帧的数据负载内部运行。
