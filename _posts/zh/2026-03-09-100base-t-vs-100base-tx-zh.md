---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 100BASE-T 与 100BASE-TX 详解
translated: true
type: note
---

问题：100BASE-TX 和 100BASE-T 有什么区别？问题：100BASE-T 和 100BASE-TX 有什么区别？

答案：

## 简短回答

**100BASE-T** 和 **100BASE-TX** 在大多数实际使用中基本上是同一件事。从技术上讲，**100BASE-T** 是**总称/通用术语**，涵盖所有 Fast Ethernet 铜缆标准，而 **100BASE-TX** 是该伞下的一个**特定子集**。

---

## 100BASE-T — 家族名称

**100BASE-T** 是一个技术术语，定义了支持 twisted pair 电缆上 100 Mbps 网络的**物理层 (PHY) 标准家族**。根据 1995 年发布的 IEEE 802.3u 标准，它定义了三种具体的 100 Mbps 以太网变体：**100BASE-TX**、**100BASE-T4** 和 **100BASE-T2**。

因此，将 **100BASE-T** 视为一个**类别**，而非单一标准。

---

## 100BASE-TX — 特定标准

**100BASE-TX** 是 Fast Ethernet 的**主流且最受欢迎**形式。它运行在 Category 5 或更高电缆内的**两对线**上，节点间最大电缆距离为**100 米**。一对线用于每个方向，提供每个方向 100 Mbps 的**full-duplex** 操作。

“TX”（有时简称为“T”）表示它是使用**四对可用线中的两对**的 Cat5 UTP 直通电缆，支持高达 100 Mbps 的速度。

---

## 100BASE-T 家族的其他成员呢？

| 标准 | 使用的线对数 | 所需电缆 | 备注 |
|---|---|---|---|
| **100BASE-TX** | 2 pairs | Cat5 或以上 | 最常见；到处使用 |
| **100BASE-T4** | 4 pairs | Cat3 或以上 | 较旧；设计用于较低质量电缆 |
| **100BASE-T2** | 2 pairs | Cat3 或以上 | 罕见；基本未使用 |
| **100BASE-FX** | N/A (fiber) | Multimode fiber | 非铜缆；使用光信号 |

T4 变体使用 Cat5 UTP 电缆中的**所有四对线**，并支持高达 100 Mbps 的速度，最大长度同样为 100 米。

---

## 关键要点

**100BASE-T** 这个术语有时可能以更广义的方式使用，或指代 Fast Ethernet 的早期/不太具体的实现，而 **100BASE-TX** 精确指代要求使用**Category 5 布线**的两对 twisted pair 上 100 Mbps 以太网的标准。在许多实际讨论中，**100BASE-T** 和 **100BASE-TX** 被**互换使用**来指代同一事物。

简而言之：
- **100BASE-T** = twisted pair 上的整个 Fast Ethernet 家族
- **100BASE-TX** = 该家族中特定、最广泛使用的成员

参考资料：

- [Fast Ethernet – Wikipedia](https://en.wikipedia.org/wiki/Fast_Ethernet)
- [100BaseTX: Implementation and Troubleshooting – Network Encyclopedia](https://networkencyclopedia.com/100basetx/)
- [100Base-TX/T4/FX – Firewall.cx](https://www.firewall.cx/networking/network-cabling/network-cabling-100basetx.html)
- [Difference between 100BaseT & 100BaseTX – Cisco Community](https://community.cisco.com/t5/other-network-architecture-subjects/difference-between-100baset-100basetx/td-p/240154)
