---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解数据链路层
translated: true
type: note
---

**问题：** 我如何理解数据链路层？

**答案：**

## 概述

**数据链路层**是 OSI（开放系统互连）模型的**第2层**。它位于物理层（第1层）和网络层（第3层）之间。其核心任务是在单个物理链路上提供**可靠的节点到节点数据传输**。

---

## 主要职责

| 功能 | 描述 |
| --- | --- |
| **Framing** | 将原始比特封装成称为*帧*的结构化单元 |
| **Physical Addressing** | 使用 MAC 地址标识本地网络上的源/目标 |
| **Error Detection** | 利用 CRC、校验和检测（有时纠正）传输错误 |
| **Flow Control** | 防止快速发送方压垮慢速接收方 |
| **Access Control** | 确定谁可以使用共享信道（例如以太网中的 CSMA/CD） |

---

## 两个子层

数据链路层分为两个子层：

```
┌─────────────────────────────────────────┐
│  LLC（逻辑链路控制）— IEEE 802.2        │  ← 与网络层通信
├─────────────────────────────────────────┤
│  MAC（介质访问控制）                     │  ← 与物理层通信
└─────────────────────────────────────────┘
```

- **LLC**：处理流控制、错误校验和协议复用
- **MAC**：处理对物理介质的访问以及 MAC 寻址

---

## 帧结构（以太网示例）

```
┌──────────┬──────────┬──────┬──────────────┬─────┐
│ Preamble │ Dest MAC │ Src  │   Payload    │ CRC │
│ 8 bytes  │ 6 bytes  │ MAC  │ 46–1500 bytes│ 4 B │
│          │          │ 6 B  │              │     │
└──────────┴──────────┴──────┴──────────────┴─────┘
```

- **Preamble**：同步比特
- **MAC 地址**：48 位硬件地址（例如 `AA:BB:CC:DD:EE:FF`）
- **Payload**：来自第3层的实际数据（IP 数据包）
- **CRC**：用于错误检测的循环冗余校验

---

## 常见协议

| 协议 | 使用场景 |
| --- | --- |
| **Ethernet (802.3)** | 有线局域网 |
| **Wi-Fi (802.11)** | 无线局域网 |
| **PPP** | 点对点链路（例如 DSL） |
| **HDLC** | 串行通信 |
| **ARP** | 解析 IP → MAC 地址 |

---

## 关键设备

- **交换机**（第2层设备）：基于 MAC 地址表转发帧
- **网桥**：在第2层连接两个网段
- **NIC（网络接口卡）**：具有烧录的 MAC 地址

---

## 在 OSI 模型中的位置

```
第7层  应用层
第6层  表示层
第5层  会话层
第4层  传输层
第3层  网络层      ← IP 数据包
─────────────────────
第2层  数据链路层    ← 帧 + MAC 地址  ← 你在这里
第1层  物理层       ← 原始比特（0 和 1）
```

---

## 心智模型

将数据链路层想象为**同一栋建筑内的本地邮政服务**：

- **物理层**是走廊/线缆
- **数据链路层**是内部邮件系统，知道房间号（MAC 地址）并在房间之间可靠地递送信封（帧）
- **网络层**处理建筑之间（不同网络）的路由

---

**参考文献：**

- [OSI 模型 – 数据链路层 (Cloudflare)](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
- [数据链路层 – Wikipedia](https://en.wikipedia.org/wiki/Data_link_layer)
- [以太网帧结构 – GeeksForGeeks](https://www.geeksforgeeks.org/ethernet-frame-format/)
- [计算机网络：自顶向下方法 (Kurose & Ross)](https://gaia.cs.umass.edu/kurose_ross/index.php)
