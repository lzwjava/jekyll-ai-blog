---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 路由器工作在网络层
translated: true
type: note
---

问题：在 **OSI** 七层参考模型中，**routers** 和 **bridges** 都是网络互联设备，但它们工作在不同的层。**Router** 在哪一层工作？
A. Network Layer
B. Transport Layer
C. Session Layer
D. Application Layer

答案：

## 答案：A — Network Layer

### 解释

这个题目考察你对常见网络设备在 **OSI (Open Systems Interconnection) 7-layer model** 中工作位置的理解。

---

### OSI 模型概述（相关层）

| Layer | Name | Example Devices |
| --- | --- | --- |
| Layer 1 | Physical Layer | Hub, Repeater |
| Layer 2 | Data Link Layer | **Bridge**, Switch |
| Layer 3 | Network Layer | **Router** |
| Layer 4 | Transport Layer | Gateway (partial) |

---

### 关键比较：Bridge 与 Router

| 特性 | Bridge | Router |
| --- | --- | --- |
| OSI Layer | **Layer 2 — Data Link Layer** | **Layer 3 — Network Layer** |
| Address Used | **MAC Address** (Physical Address) | **IP Address** (Logical Address) |
| Function | 在同一网络中转发或过滤 **frames** | 在不同网络之间转发 **packets** |
| Network Scope | 同一 LAN / 网络段 | 不同网络 / 子网 |
| Intelligence | 智能较低，简单转发 | 更智能，使用 routing tables |

---

### 为什么 Router 在 Network Layer 工作

- **Router** 读取数据包头部中的 **destination IP address** 来做出转发决策。
- 它使用 **routing tables** 和 **protocols**（例如，RIP、OSPF、BGP）来确定最佳路径。
- 它可以连接 **heterogeneous networks**（不同网络架构）。
- 因为 **IP addressing** 是 OSI 模型中 **Layer 3 (Network Layer)** 的功能，因此 **routers** 被归类为 Layer 3 设备。

---

### 为什么选项 A 正确

- **A (Network Layer)** ✅ — **Routers** 在这里工作，使用 **IP addresses** 来路由 **packets**。
- **B (Transport Layer)** ❌ — 这个层处理端到端通信（**TCP/UDP**）；没有标准路由设备在这里工作。
- **C (Session Layer)** ❌ — 管理应用之间会话；没有路由设备在这里工作。
- **D (Application Layer)** ❌ — 这是面向用户的最高层协议（**HTTP**、**FTP** 等）。

---

### 总结

> **Bridge** 在 **Data Link Layer (Layer 2)** 工作，使用 **MAC addresses**，而 **router** 在 **Network Layer (Layer 3)** 工作，使用 **IP addresses**。这是网络考试中经典且经常考察的区别。
