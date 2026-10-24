---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SRAM：静态随机存取存储器
translated: true
type: note
---

问题：缩写SRAM代表什么？它是什么？

回答：**SRAM** 代表 **Static Random-Access Memory**。它是一种具有两个主要特性的计算机内存：

- **Static** — 只要有电源供应，它就能保留数据，无需周期性刷新（这与必须不断刷新的DRAM不同）。
- **Random-Access** — 任何内存位置都可以在大致相同的时间内被读取或写入，无论其物理位置如何。

**工作原理：** 每个比特通过一个称为 *bistable latch*（通常由6个晶体管组成）的电路来存储，该电路会稳定地保持其状态，直到断电或该比特被覆盖。

**与DRAM相比的主要特性：**

| | SRAM | DRAM |
|---|---|---|
| 速度 | 更快 | 更慢 |
| 成本 | 更高 | 更低 |
| 密度 | 更低（每比特晶体管更多） | 更高 |
| 需要刷新？ | 否 | 是 |
| 典型用途 | CPU缓存 (L1/L2/L3) | 主系统RAM |

**常见用途：**
- CPU缓存 (L1, L2, L3)
- 微控制器中的寄存器和缓冲区
- 网络设备（路由器、交换机）
- 速度比容量更重要的嵌入式系统

参考资料：
- [Static random-access memory – Wikipedia](https://en.wikipedia.org/wiki/Static_random-access_memory)