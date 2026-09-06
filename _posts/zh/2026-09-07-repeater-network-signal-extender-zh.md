---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中继器：网络信号扩展器
translated: true
type: note
---

问题：在互联网/网络扩展设备中，“中继器”是什么？

答案：

**中继器**是一种网络设备，它**接收信号并以更高功率重新发送**，使信号能够在不衰减的情况下传输更远距离。以下是详细说明：

**核心功能**

- 工作在 OSI 模型的**第1层（物理层）**
- 它只是放大或再生信号 —— 不进行过滤、路由或解释数据
- 适用于有线和无线信号

**常见用途**

- 在大型住宅或办公室中扩展 Wi-Fi 覆盖范围（无线中继器 / Wi-Fi 扩展器）
- 将以太网线缆的传输距离延长至标准100米限制以上
- 在信号盲区增强蜂窝信号

**类型**

- **有线中继器** —— 用于较旧的同轴电缆或双绞线网络
- **无线中继器 / Wi-Fi 扩展器** —— 最常见的现代形式；通过无线方式连接到路由器并重新广播信号
- **光中继器** —— 用于光纤网络，再生光信号

**中继器 vs 类似设备**

| 设备 | OSI 层 | 智能程度 |
| --- | --- | --- |
| 中继器 | 第1层 | 无 —— 仅增强信号 |
| 桥接器 | 第2层 | 根据 MAC 地址过滤 |
| 路由器 | 第3层 | 根据 IP 地址路由 |
| 交换机 | 第2–3层 | 根据 MAC/IP 交换 |

**主要限制**：由于它会盲目地重发所有内容（包括噪声和冲突），因此不会提高网络**效率**，只会增加**覆盖范围**。

参考来源：

- [中继器 – Wikipedia](https://en.wikipedia.org/wiki/Repeater)
- [什么是网络中继器？– Cisco](https://www.cisco.com/c/en/us/products/switches/what-is-a-network-switch.html)
- [Wi-Fi 扩展器 vs 中继器 – HowToGeek](https://www.howtogeek.com/845669/wi-fi-extender-vs-repeater-whats-the-difference/)
