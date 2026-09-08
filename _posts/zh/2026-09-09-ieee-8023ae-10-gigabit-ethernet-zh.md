---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE 802.3ae 10千兆以太网
translated: true
type: note
---

**问题：** 什么是 IEEE 802.3ae，它的主要特性是什么？

**回答：**

## IEEE 802.3ae — 10 Gigabit Ethernet 简介

### 概述

IEEE 802.3ae 是定义基于光纤布线实现 10 Gigabit Ethernet (10GbE) 的基础行业标准。该标准于 2002 年作为 IEEE 802.3 CSMA/CD 协议的修订版发布，支持 10,000 Mbps 的数据传输速率。

它的推出是为了应对局域网中对更快数据传输速率日益增长的需求。在此标准之前，以太网技术主要局限于 10 Mbps、100 Mbps 和 1 Gbps 的速度。

---

### 关键特性

- **仅支持全双工：** 与之前的以太网标准不同，IEEE 802.3ae 仅支持全双工操作，且仅运行于光纤介质上。
- **向后兼容的帧结构：** 它保留了现有的以太网帧格式和 MAC 大小，确保与旧有以太网基础设施无缝集成，同时相对于千兆以太网提供十倍吞吐量的提升。
- **双 PHY 方案：** 支持用于标准 10GbE 操作的 LAN PHY，以及通过 WAN 接口子层 (WIS) 增加与 SONET/SDH 网络兼容性的 WAN PHY。

---

### 物理层变体 (PCS)

该标准规定了多个物理编码子层——**10GBASE-X**、**10GBASE-R** 和 **10GBASE-W**，以及配套接口，包括 10 Gigabit 介质无关接口 (XGMII)、10 Gigabit 连接单元接口 (XAUI) 和 10 Gigabit 十六位接口 (XSBI)。

值得注意的物理介质类型包括：

- **10GBASE-SR** — 短距离光纤 (850 nm)，适用于建筑物内连接。
- **10GBASE-LR** — 长距离光纤 (1310 nm)，专为覆盖数公里的连接设计。
- 在多模光纤上支持最远 **300 米**，在单模光纤上支持最远 **40 公里**。

---

### 主要应用场景

它主要用于骨干网络、高速数据中心和企业核心交换机，以消除高流量环境中的带宽瓶颈。

---

### 技术传承与演进

IEEE 802.3ae 的成功为后续进步铺平了道路，包括引入 40GbE 和 100GbE 的 IEEE 802.3ba，展示了该技术的持续演进。

---

**参考文献：**

- [IEEE Xplore – 802.3ae-2002 标准](https://ieeexplore.ieee.org/document/1040118)
- [IEEE SA – 802.3ae 官方页面](https://standards.ieee.org/ieee/802.3ae/1089/)
- [LINK-PP – IEEE 802.3ae 详解](https://www.link-pp.com/glossary/ieee-802-3ae.html)
- [Linden Photonics – 10GbE 标准概述](https://www.lindenphotonics.com/standards-for-10gb-ethernet-a-comprehensive-overview)
