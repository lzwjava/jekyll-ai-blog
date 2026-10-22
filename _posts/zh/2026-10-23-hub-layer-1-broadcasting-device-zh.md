---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 集线器：第一层广播设备
translated: true
type: note
---

问题：在计算机网络中，“hub”是什么意思？

答案：

**hub** 是一种基本的 Layer 1（Physical Layer）网络设备，用于连接 Local Area Network (LAN) 中的多个设备。其工作方式如下：

**核心行为：**
- 当 hub 在一个端口收到数据包时，它会将该数据包 **broadcast**（复制并发送）到 **所有其他端口**，无论目标地址是什么。
- 它没有智能——它不知道哪个设备连接在哪个端口上，也不会过滤或引导 traffic。

**关键特性：**
- 工作在 **OSI Physical Layer（Layer 1）**
- 创建一个单一的 **collision domain** —— 同一时间只能有一个设备传输，否则数据会冲突并需要重传
- 所有连接的设备共享相同的带宽
- 仅支持 half-duplex 通信

**Hub vs. Switch vs. Router：**

| Device | Layer | Traffic Handling |
|--------|-------|-----------------|
| Hub | L1 | 向所有端口 broadcast |
| Switch | L2 | 仅转发到目标 MAC address |
| Router | L3 | 使用 IP 在不同网络之间路由 |

**为什么 hub 已经过时：**
因为 hub 将一切 broadcast 到每个设备，所以会造成不必要的网络拥塞，并且存在安全风险（任何设备都可以“sniff”所有 traffic）。**Switch** 在几乎所有现代网络中取代了 hub，因为它们更智能、更快、更安全。

参考链接：
- [Network Hub – Wikipedia](https://en.wikipedia.org/wiki/Ethernet_hub)
- [Hub vs Switch vs Router – Cisco](https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/network-switch-vs-router.html)