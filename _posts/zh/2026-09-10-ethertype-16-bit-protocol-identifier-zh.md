---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EtherType：16位协议标识符
translated: true
type: note
---

**问题：** 什么是 EtherType？

**答案：**

EtherType 是以太网帧头部的一个 **两字节（16位）字段**，用于标识帧的有效载荷中封装的是哪个 **上层协议** —— 它本质上是告知接收方的网络协议栈 *如何解释后续的数据*。

**它在以太网帧中的位置：**

| 目标 MAC | 源 MAC | **EtherType** | 有效载荷 | FCS |
|---|---|---|---|---|
| 6 字节 | 6 字节 | **2 字节** | 46–1500 字节 | 4 字节 |

**双重角色——EtherType 与长度：**

在现代以太网中，这个相同的 2 字节字段根据其值的不同可以起到两种不同的作用：
- **≤ 0x05DC (1500)** → 表示有效载荷的 **长度**（IEEE 802.3 帧格式）
- **≥ 0x0600 (1536)** → 表示 **EtherType** / 协议标识符（Ethernet II 帧格式）

**谁负责分配 EtherType 值？**

EtherType 值由 **IEEE 注册机构** 分配。

**常见的 EtherType 值：**

| EtherType | 协议 |
|-----------|------|
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN 标签（IEEE 802.1Q） |
| `0x8847` | MPLS 单播 |
| `0x88CC` | LLDP |

**实际工作原理：**

当网卡接收到一个以太网帧时，它会读取 EtherType 字段，并将有效载荷交给正确的协议处理程序——例如，如果 EtherType 是 `0x0800`，则有效载荷会被传递给 IP 协议栈。

EtherType 是 16 位的标识符，出现在 MAC 目的地址和源地址之后（或在标签之后）的前两个字节中，当将其视为无符号整数时，其值大于或等于 0x0600。

**参考资料：**
- [EtherType – 维基百科](https://en.wikipedia.org/wiki/EtherType)
- [RFC 7042 – IEEE 802 参数的 IANA 考量](https://datatracker.ietf.org/doc/rfc7042/)
- [EtherType – Networx 安全术语表](https://www.networxsecurity.org/members-area/glossary/e/ethertype.html)