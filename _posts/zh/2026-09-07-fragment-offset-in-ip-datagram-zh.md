---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IP数据报中的分片偏移
translated: true
type: note
---

Question: IP数据报中的Fragment Offset字段是什么？

Answer:

**Fragment Offset**字段是IPv4头部中的一个13位字段，用于指示某个分片在原始（未分片）数据报中的位置。

**关键细节：**

- **大小：** 13位
- **单位：** 以**8字节**（64位）为单位，因此实际字节偏移量 = 字段值 × 8
- **目的：** 允许目的主机按正确顺序重组分片，即使它们乱序到达

**工作原理：**

当路由器需要分片一个较大的IP数据报时（因为其超过下一链路的MTU）：

1. 将数据拆分为较小的分片
2. 每个分片获得**相同的Identification号**（以便目的主机知道它们属于同一数据报）
3. 每个分片获得一个**Fragment Offset**值，指示其在原始数据中的位置
4. 除最后一个分片外，所有分片的**More Fragments (MF)标志**设置为1

**示例：**

假设原始数据报有4000字节数据，分为3个分片：

| 分片 | 数据字节范围 | 偏移值（÷8） |
| --- | --- | --- |
| 第1个 | 0–1479 | 0 |
| 第2个 | 1480–2959 | 185 |
| 第3个 | 2960–3999 | 370 |

目的主机使用偏移值按正确顺序重建原始数据报。

参考资料：

- [RFC 791 – Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [Computer Networking: A Top-Down Approach – Kurose & Ross, 第4章](https://gaia.cs.umass.edu/kurose_ross/index.php)
