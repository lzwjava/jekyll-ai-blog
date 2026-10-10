---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 10BASE-T集线器节点距离
translated: true
type: note
---

**问题：** 什么是10BASE-T？集线器与节点之间的最大距离是多少？

**答案：**

**10BASE-T 概述**

10BASE-T 是 IEEE 802.3i（1990年）定义的一种早期以太网标准。名称分解如下：

| 部分 | 含义 |
| ------ | ------ |
| **10** | 10 Mbps 数据速率 |
| **BASE** | 基带信号传输 |
| **T** | 双绞线（UTP）电缆 |

关键特性：

- **拓扑结构：** 星型（每个节点单独连接至中央集线器）
- **电缆：** 非屏蔽双绞线（UTP），Cat 3 或更高等级
- **连接器：** RJ-45
- **双工模式：** 半双工（基于集线器）；使用交换机可实现全双工
- **信号：** 曼彻斯特编码

---

**最大距离：集线器 ↔ 节点**

> **每段 100 米（328 英尺）**

这是从集线器（或交换机）端口到任何单个节点（PC、打印机等）的最大电缆长度。超过 100 米时，信号衰减会导致错误。

为了延长覆盖范围，可以级联集线器——但整个网络需遵循 **5-4-3 规则**：

- 最多 **5** 个网段
- 由 **4** 个中继器/集线器连接
- 只有 **3** 个网段可连接活动节点

---

**参考资料：**

- [IEEE 802.3 标准概述 – IEEE](https://www.ieee802.org/3/)
- [10BASE-T – 维基百科](https://en.wikipedia.org/wiki/10BASE-T)
- [以太网布线标准 – Cisco](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/12006-ethernet-00.html)
