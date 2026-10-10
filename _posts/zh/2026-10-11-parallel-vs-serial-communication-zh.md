---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行与串行通信
translated: true
type: note
---

**问题：** 并行通信（并行通信）与串行通信（串行通信）有哪些异同点？

---

**回答：**

## 相似点

- 两者都是设备间传输数字数据的方法
- 两者均可工作于**同步**或**异步**模式
- 两者都要求发送方与接收方约定通信协议
- 两者均应用于计算机硬件、嵌入式系统及网络通信中

---

## 不同点

| 方面 | 并行 (Parallel) | 串行 (Serial) |
| --- | --- | --- |
| **数据线** | 多条导线（例如一次传输8、16、32位） | 单条导线（一次传输1位） |
| **短距离速度** | 更快——每个时钟周期传输多个位 | 每周期较慢，但现代串行速度极快 |
| **长距离速度** | 衰减——信号偏移与串扰问题 | 更优——长距离下保持信号完整性 |
| **成本 / 复杂度** | 更昂贵——需要更多引脚、线缆、连接器 | 更便宜——导线和连接器更少 |
| **干扰** | 高——并行线路易产生**串扰 (crosstalk)** | 低——干扰极小 |
| **同步** | 要求所有线路同步（时钟偏移问题） | 单线路更易同步 |
| **距离** | 仅限短距离（如内部总线） | 短距离至极长距离均可 |
| **实例** | 旧式打印机端口 (LPT)、IDE/PATA、PCI | USB、SATA、以太网、RS-232、I²C、SPI、UART |

---

## 关键洞察

具有讽刺意味的是，**现代串行接口（如 USB 3.x、PCIe、SATA）如今比旧式并行接口更快**——因为消除了串扰问题，时钟频率得以大幅提升。这也是 PC 中并行端口几乎被串行连接完全取代的原因。

> **经验法则：** 并行在*短突发传输的简单性*上占优；串行在*速度、距离与可扩展性*上胜出。

---

**参考资料：**

- [Serial vs. Parallel Communication – Wikipedia](https://en.wikipedia.org/wiki/Serial_communication)
- [Parallel Communication – Wikipedia](https://en.wikipedia.org/wiki/Parallel_communication)
- [Why Serial Replaced Parallel – All About Circuits](https://www.allaboutcircuits.com/technical-articles/why-serial-replaced-parallel/)
