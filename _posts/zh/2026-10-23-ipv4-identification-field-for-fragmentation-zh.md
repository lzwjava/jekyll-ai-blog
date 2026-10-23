---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv4 分片标识字段
translated: true
type: note
---

问题：IP数据报中的“标识字段”（Identification field）是什么？

答案：

**标识字段**（Identification field）是IPv4头部中的一个**16比特字段**，主要用于**IP分片与重组**（IP fragmentation and reassembly）。

---

### 作用与用途

当IP数据报太大而无法适应网络链路的**MTU（最大传输单元）**时，它会被**分片（fragmented）**成更小的片段。标识字段作为一个**共享标签**，将所有属于同一原始数据报的片段连接起来，以便目的主机能正确地重组它们。

---

### 主要特性

| 属性 | 详情 |
| --- | --- |
| 大小 | 16 bits |
| 头部位置 | Bytes 4–5 of the IPv4 header |
| 分配者 | **发送主机**（通常是一个 incrementing counter） |
| 范围 | Unique per (source IP, destination IP, protocol) pair — within a reasonable time window |

---

### 工作原理（分片示例）

```
Original datagram (4000 bytes, ID = 1234)
         ↓  fragmented at router
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ ID=1234  Frag 1 │  │ ID=1234  Frag 2 │  │ ID=1234  Frag 3 │
│ Offset=0        │  │ Offset=185      │  │ Offset=370      │
│ MF=1            │  │ MF=1            │  │ MF=0 (last)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         ↓  destination reassembles using ID + Fragment Offset + MF flag
         Original datagram (4000 bytes, ID = 1234)
```

所有三个片段共享**相同的ID（1234）**，因此接收方知道它们属于同一个数据报。

---

### 相关头部字段（与ID协同工作）

- **Fragment Offset**（13 bits）— 该 fragment 在 original datagram 中的位置
- **More Fragments (MF) flag**（1 bit）— `1` = more fragments follow；`0` = this is the last one
- **Don't Fragment (DF) flag**（1 bit）— 若 set，datagram 不得被 fragmented；若太大，则被 dropped 并返回一个 ICMP error

---

### 注意事项

- 若 **DF=1**，Identification field 在 fragmentation 技术上是未使用的，但它仍存在于 header 中。
- 在 **IPv6** 中，fragmentation by routers 被消除；fragmentation 仅由 source host 使用一个 **extension header** 处理，identification concept 也被移至那里。
- 16位 space（65,536 values）理论上可能在高速 links 上 wrap around，这是一个已知的限制（[RFC 6864](https://datatracker.ietf.org/doc/html/rfc6864) discusses this）。

参考文献：

- [RFC 791 – Internet Protocol (IPv4 specification)](https://datatracker.ietf.org/doc/html/rfc791)
- [RFC 6864 – Updated Specification of the IPv4 ID Field](https://datatracker.ietf.org/doc/html/rfc6864)
