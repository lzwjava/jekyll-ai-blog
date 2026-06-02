---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分组交换类型解析
translated: true
type: note
---

在分组交换网络中，**分组交换主要有两种类型**：

1. **数据报分组交换 (Datagram Packet Switching)**
   - 每个分组独立处理。
   - 分组可能通过不同路径到达目的地。
   - 不需要预先建立路径或连接。
   - 适用于无连接通信（如 IP 网络）。

2. **虚电路分组交换 (Virtual Circuit Packet Switching)**
   - 数据传输前建立逻辑连接（虚电路）。
   - 所有分组沿相同路径传输。
   - 分组按顺序送达。
   - 适用于面向连接的通信（如 ATM 网络）。

### 关键区别

- **数据报**：无固定路径，分组独立路由。
- **虚电路**：固定路径，分组沿相同路由传输，确保有序送达。

因此，题目中的空白应正确填写为“**虚电路** (Virtual Circuit)”。
