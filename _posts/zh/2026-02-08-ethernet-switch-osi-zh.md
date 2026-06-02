---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: OSI模型中的以太网交换机
translated: true
type: note
---

该问题询问 Ethernet switch 在 OSI model 的哪一层运行。

## 正确答案：**B (Data Link Layer)**

### 解析

**Ethernet switch** 是一种多端口网络桥接器，运行在 OSI 七层参考模型的 **Layer 2 (Data Link Layer)**。

### 为什么是 Data Link Layer？

**Ethernet switches 的主要特征：**

- **MAC Address 处理**：Switch 根据 **MAC addresses**（物理地址）做出转发决策，而 MAC 地址定义在 Layer 2
- **Frame 转发**：它们根据 Frame 中的目标 MAC address 将 Ethernet frames 从一个端口转发到另一个端口
- **学习与过滤**：Switch 从传入的 Frame 中学习 MAC addresses，并构建 MAC address tables 以确定转发路径
- **不涉及 IP Address**：与 Routers（Layer 3 设备）不同，Switch 不会检查 IP addresses

### 为什么不是其他层？

- **Physical Layer (A)**：Hubs 运行在这一层，而不是 Switch
- **Network Layer (C)**：Routers 运行在这一层，根据 IP addresses 做出决策
- **Transport Layer (D)**：这一层处理端到端通信以及 TCP/UDP 等 Protocols

### 补充说明

Ethernet switches 也被称为 **Layer 2 switches** 或 **Layer 2 devices**，因为它们专门运行在 Data Link Layer。这使得它们比 Hubs 更智能，但在网络层路由能力上不如 Routers。

**恭喜！您的回答正确！ ✓**
