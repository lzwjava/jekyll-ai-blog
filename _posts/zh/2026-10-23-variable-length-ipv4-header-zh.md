---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可变长度 IPv4 报头
translated: true
type: note
---

**问题：** 在IPv4 datagram中，header（首部）的长度是多少？

**答案：**

IPv4 header的长度是**可变的**，由**IHL（Internet Header Length）**字段决定 — 这是一个4位字段，以**32位（4字节）字**为单位指定头部大小。

| 参数 | 值 |
| --- | --- |
| 最小header长度 | **20字节**（160位） — 无选项 |
| 最大header长度 | **60字节**（480位） — 有选项 |
| IHL字段大小 | 4位 → 值5–15 |
| 单位 | 32位字（每字4字节） |

**关键细节：**

- **IHL = 5** → 5 × 4 = **20字节**（最常见情况，无选项）
- **IHL = 15** → 15 × 4 = **60字节**（最大值，选项完全填充）
- header**必须始终是4字节的倍数**；必要时添加填充。

header的固定部分始终为20字节，包括Version、IHL、TTL、Protocol、Source/Destination IP等字段。可选部分（0–40字节）涵盖timestamps、routing options和security等内容。

---

**参考：**

- [RFC 791 – Internet Protocol (IPv4)](https://www.rfc-editor.org/rfc/rfc791)
- [IPv4 – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Header)
