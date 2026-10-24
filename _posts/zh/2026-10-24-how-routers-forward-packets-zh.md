---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 路由器如何转发数据包
translated: true
type: note
---

问题：路由器如何工作，以及它如何转发（retransmit）数据包？

答案：

## 路由器工作原理

一个路由器是一个 **Layer 3 (Network Layer)** 设备，它连接不同的网络并根据 **IP 地址** 在它们之间转发数据包。

### 核心组件

| 组件 | 作用 |
| --- | --- |
| **Routing Table** | 将目的网络映射到下一跳/出接口 |
| **Forwarding Engine** | 以线速移动数据包的硬件 |
| **ARP Cache** | 将 IP 地址映射到下一跳的 MAC 地址 |
| **Routing Protocol** | 构建/更新路由表（OSPF, BGP, RIP…） |

---

## 数据包转发逐步说明

以下是详细步骤：

---

### ① 接收数据包 — 剥离 L2 帧

当数据包到达路由器接口时，路由器**剥离 Ethernet (Layer 2) 帧** — 移除 MAC 地址头部。留下的是原始 **IP 数据包** (Layer 3)。

---

### ② 读取 IP 头部 — 递减 TTL

路由器读取：

- **Destination IP address** — 决定发送到哪里
- **TTL (Time To Live)** — 每经过一跳减 1

如果 TTL 减至 **0**，数据包被丢弃，并发送 **ICMP "Time Exceeded"** 消息回源。这防止了无限路由循环。

---

### ③ 路由表查找（核心决策）

路由器查询其 **routing table**，使用 **longest prefix match**：

| 目标网络 | 下一跳 | 接口 |
| --- | --- | --- |
| `10.0.0.0/8` | — | `eth1` |
| `192.168.0.0/16` | `10.0.0.1` | `eth0` |
| `0.0.0.0/0` | `203.0.1.1` | `eth2` (默认) |

最具体的匹配前缀胜出。路由器通过以下方式学习这些条目：

- **Static routes** — 手动配置
- **Dynamic protocols** — OSPF, BGP, RIP（路由器之间交换路由信息）

---

### ④ ARP + Re-encapsulate into a new L2 frame

路由表给出 **next-hop IP**，但要在线上实际发送，路由器需要 **MAC address**。它使用 **ARP (Address Resolution Protocol)** 将 next-hop IP 解析为 MAC，然后将 **IP packet 包装在全新的 Ethernet frame** 中，包含：

- **New source MAC** = 路由器出接口的 MAC
- **New dest MAC** = 下一跳设备的 MAC

> IP packet 本身不变（source/dest IPs 相同），仅 L2 wrapper 被替换。

---

### ⑤ Transmit

新 frame 通过正确的物理接口发送到下一跳。该过程在每个路由器重复，直到 packet 到达其目的地。

---

### 关键区别：Routers 不会 "retransmit" — end hosts 会

Routers **forward**（而不是 retransmit）。如果 router **drops** 一个 packet（queue full, TTL expired, no matching route），它会 silently drop 它（或 send ICMP error）。**TCP retransmission** 完全由 **sender** 处理 — 它通过 timeout 或 duplicate ACKs 检测 loss 并 resend。

---

参考资料：

- [RFC 791 — Internet Protocol (IP)](https://datatracker.ietf.org/doc/html/rfc791)
- [RFC 826 — ARP](https://datatracker.ietf.org/doc/html/rfc826)
- [RFC 792 — ICMP](https://datatracker.ietf.org/doc/html/rfc792)
