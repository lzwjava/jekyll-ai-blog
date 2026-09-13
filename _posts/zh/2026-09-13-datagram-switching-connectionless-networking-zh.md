---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据报交换：无连接网络
translated: true
type: note
---

Question: "datagram switching"（数据报交换）属于无连接通信模型吗？

Answer: 是的，datagram switching 是一种**无连接**的分组交换技术。原因如下：

**工作原理：**

- 每个数据包（datagram）被**独立**处理
- 每个数据包携带**完整的目的地址**
- 数据包可能通过网络中的**不同路径**传输
- 它们可能**乱序**到达，并需要在目的地重新排序

**为什么是无连接的：**

- 发送数据**之前**没有建立专用路径
- 不需要“握手”或建立阶段
- 网络动态地为每个数据包做出路由决策
- 在网络层，发送方和接收方之间**不维护状态**

**与面向连接（虚电路交换）的对比：**

| 特性 | Datagram（无连接） | Virtual Circuit（面向连接） |
| --- | --- | --- |
| 路径建立 | 无 | 传输前需要 |
| 路由 | 逐包 | 逐连接 |
| 数据包顺序 | 可能变化 | 保持不变 |
| 示例 | IP（Internet Protocol） | ATM, Frame Relay |

实际中 datagram switching 的经典例子是互联网的 **IP 层**——数据包独立路由，不保证顺序或送达。

参考文献：

- [Connectionless vs Connection-oriented – Forouzan, Data Communications and Networking](https://www.mheducation.com/highered/product/data-communications-networking-forouzan/M9780073376226.html)
- [Datagram vs Virtual Circuit – Techopedia](https://www.techopedia.com/definition/25449/datagram)
- [IP as a Connectionless Protocol – Cloudflare](https://www.cloudflare.com/learning/network-layer/internet-protocol/)
