---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 万兆以太网传输介质
translated: true
type: note
---

**问题：** 10吉比特以太网（万兆位以太网）支持哪些传输介质/方式？

**答案：**

10吉比特以太网（10GbE，IEEE 802.3ae / 802.3an）支持**多种传输介质**，分为两大类：

---

### 🔵 光纤（Optical Fiber）

| 标准 | 光纤类型 | 最大距离 |
| --- | --- | --- |
| **10GBASE-SR** | 多模光纤（MMF） | 26–400 m |
| **10GBASE-LR** | 单模光纤（SMF） | 10 km |
| **10GBASE-ER** | 单模光纤（SMF） | 40 km |
| **10GBASE-ZR** | 单模光纤（SMF） | 80 km |
| **10GBASE-LX4** | 多模/单模光纤 | 300 m / 10 km |

---

### 🟡 铜缆（Copper）

| 标准 | 介质 | 最大距离 |
| --- | --- | --- |
| **10GBASE-T**（802.3an） | Cat 6a / Cat 7 UTP | 100 m |
| **10GBASE-CX4** | 双轴铜缆 | 15 m |
| **10GBASE-CR / DAC** | 直连铜缆（SFP+） | 1–7 m |

---

### 关键要点

- **10GBASE-T** 是最常见的铜缆解决方案，需要**Cat 6a或更高级别**的布线（千兆以太网仅需Cat 5e）。
- **光纤** 更适用于长距离或数据中心骨干网络。
- **DAC（直连铜缆）** 因成本低、延迟低，常用于短距离机架间连接。
- 所有变体均以**10 Gbps**全双工速率运行。

---

**参考资料：**

- [10 Gigabit Ethernet – Wikipedia](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet)
- [IEEE 802.3an (10GBASE-T)](https://en.wikipedia.org/wiki/10GBASE-T)
