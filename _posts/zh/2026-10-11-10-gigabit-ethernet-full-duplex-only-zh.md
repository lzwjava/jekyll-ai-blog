---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 10千兆位以太网全双工仅限
translated: true
type: note
---

**问题：** 万兆位以太网 (10 Gigabit Ethernet) 以全双工还是半双工模式运行？

**答案：**

**万兆位以太网仅支持全双工模式。**

| 属性 | 详情 |
| --- | --- |
| **模式** | **仅**全双工 |
| **半双工** | ❌ 不支持 |
| **CSMA/CD** | ❌ 不使用（无需碰撞检测） |
| **同时发送/接收** | ✅ 可同时以 10 Gbps 速率收发 |

---

### 为什么没有半双工？

- 万兆位以太网 **专为交换网络设计** —— 每台设备点对点连接至交换机，因此不存在共享介质，也不会产生碰撞。
- **CSMA/CD**（半双工以太网中使用的碰撞检测机制）在 10 Gbps 标准中**已被正式移除**。
- 这适用于**所有**万兆位以太网变体 —— 光纤（10GBASE-SR/LR/ER）和铜缆（10GBASE-T/CX4/DAC）。

> 注：半双工在千兆位以太网（1000BASE-T）中已逐渐少见，并在万兆位以太网中完全被淘汰。

---

**参考资料：**

- [万兆位以太网 – Wikipedia](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet)
- [IEEE 802.3ae 标准概述](https://standards.ieee.org/ieee/802.3ae/1768/)
