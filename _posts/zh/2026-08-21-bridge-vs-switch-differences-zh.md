---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网桥与交换机的区别
translated: true
type: note
---

Question: Bridge 和 Switch 有什么区别？

Answer:

两者都工作在 **Layer 2 (Data Link Layer)**，使用 MAC 地址转发帧，但它们在几个方面有所不同：

| Feature | Bridge | Switch |
| --- | --- | --- |
| **Ports** | 通常 2–4 个端口 | 多个端口（8、24、48…） |
| **Processing** | 基于软件 | 基于硬件（ASIC） |
| **Speed** | 较慢 | 快得多 |
| **Forwarding** | 仅存储转发 | 存储转发 + 直通转发 |
| **Collision domains** | 每个端口一个 | 每个端口一个 |
| **Usage today** | 基本已淘汰 | 现代网络标准方案 |

**关键点：** Switch 本质上是一个 **多端口 Bridge**——它执行相同的工作（学习 MAC 地址，在网段之间过滤/转发帧），但规模和速度要大得多。

历史上，Bridge 用于连接两个 LAN 网段。Switch 通过将相同的逻辑应用于每个端口来取代它们，使每个设备拥有自己独立的冲突域。

> 两者仍然在每个 VLAN 中共享一个广播域，这就是为什么需要路由器（Layer 3）来分隔广播流量。

参考：

- [Network Bridge - Wikipedia](https://en.wikipedia.org/wiki/Network_bridge)
- [Network Switch - Wikipedia](https://en.wikipedia.org/wiki/Network_switch)
