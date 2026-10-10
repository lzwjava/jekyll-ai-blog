---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速以太网：100 Mbps 标准
translated: true
type: note
---

Question: 什么是快速以太网（Fast Ethernet），它的速度有多快？

Answer: **快速以太网（Fast Ethernet）** 是一种网络标准，运行速度为 **100 Mbps（兆比特每秒）**——正好是原始以太网标准（10 Mbps）的 10 倍。

**关键事实：**

- **官方标准：** IEEE 802.3u（1995 年批准）
- **速度：** 100 Mbps
- **常见变体：**
  - **100BASE-TX** —— 运行在 Cat 5（或更好）双绞线铜缆上；部署最广泛的变体
  - **100BASE-FX** —— 运行在光纤电缆上
  - **100BASE-T4** —— 使用 4 对 Cat 3 电缆（基本已淘汰）
- **最大段长度：** 铜缆（100BASE-TX）100 米，光纤（100BASE-FX）可达 2 公里
- **双工模式：** 支持半双工和全双工模式（全双工可提供 200 Mbps 的总聚合带宽）

**速度对比：**

| 标准 | 中文名称 | 速度 |
|---|---|---|
| Ethernet | 以太网 | 10 Mbps |
| **Fast Ethernet** | **快速以太网** | **100 Mbps** |
| Gigabit Ethernet | 千兆以太网 | 1,000 Mbps |
| 10 Gigabit Ethernet | 万兆以太网 | 10,000 Mbps |

快速以太网在 1990 年代末至 2000 年代是主流的局域网标准。如今它已在很大程度上被**千兆以太网（Gigabit Ethernet）**取代，不过在较旧的硬件和一些嵌入式设备上仍能看到 100BASE-TX 端口。

参考：
- [IEEE 802.3u – Fast Ethernet Standard](https://standards.ieee.org/ieee/802.3u/1119/)
- [Fast Ethernet – Wikipedia](https://en.wikipedia.org/wiki/Fast_Ethernet)