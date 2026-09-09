---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 0x0600 EtherType阈值
translated: true
type: note
---

**问题：** 在IEEE 802（以太网）语境中，0x0600（0x600）意味着什么？

**答案：**

`0x0600`（十进制1536）本身并不是一个已分配的EtherType值——而是以太网中区分EtherType帧与基于长度帧的**边界阈值**。

含义如下：

**阈值规则：**
统一标准IEEE 802.3x-1997要求EtherType值大于或等于1536（0x0600）。选择该值是因为以太网802.3帧的数据字段最大长度（MTU）为1500字节（0x05DC）。因此，1500及以下的值表示该字段代表**有效载荷的大小**，而1536及以上的值表示该字段代表一个**EtherType**（协议标识符）。1501–1535之间的值未定义。

**为何重要：**
- **≤ 0x05DC（1500）** → 该字段是**长度**字段（IEEE 802.3帧格式）
- **≥ 0x0600（1536）** → 该字段是**EtherType**（协议标识符，Ethernet II帧格式）
- **0x0601–0x05FF** → 未定义/保留间隙

**常见大于0x0600的EtherType示例：**

| EtherType | 协议 |
|-----------|------|
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN（802.1Q） |

简而言之，`0x0600`是有效EtherType的**最小边界值**——它是一个设计标记，本身并非协议分配。

**参考资料：**
- [EtherType – Wikipedia](https://en.wikipedia.org/wiki/EtherType)
- [RFC 7042 – IEEE 802 Parameters (IETF)](https://datatracker.ietf.org/doc/rfc7042/)
- [EtherType – Networx Security](https://www.networxsecurity.org/members-area/glossary/e/ethertype.html)