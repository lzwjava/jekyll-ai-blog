---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 交换机按层分类
translated: true
type: note
---

问题：根据交换机处理的协议层，交换机分为哪几类？（填空：二层交换机和______。）

答案：**三层交换机（Layer 3 Switches）**

交换机根据其在OSI模型中的工作层级进行分类：

- **二层交换机（Layer 2 Switch）：** 工作在数据链路层。它使用**MAC地址**在同一网段（局域网）内转发帧。无法在不同子网之间路由流量。

- **三层交换机（Layer 3 Switch）：** 同时工作在数据链路层和**网络层**。除MAC地址外，还使用**IP地址**，能够执行**VLAN间路由**，并在不同子网之间转发数据包——集传统交换机与路由器功能于一体。

| 特性 | 二层交换机 | 三层交换机 |
| --- | --- | --- |
| OSI层级 | 第二层（数据链路层） | 第二层 + 第三层（网络层） |
| 使用地址 | MAC地址 | MAC地址 + IP地址 |
| 路由能力 | ✗ | ✓ |
| VLAN间路由 | ✗ | ✓ |
| 速度 | 非常快 | 快（基于硬件的路由） |

> 在某些场景下，还会提及**四层交换机（Layer 4 Switches）**，它能够额外检查传输层信息（TCP/UDP端口）以实现更高级的流量管理。

---

参考来源：

- [OSI模型与网络交换机 - Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-a-network-switch.html)
- [三层交换机与路由器对比 - NetworkLessons](https://networklessons.com/switching/layer-3-switch)
