---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络位和主机容量
translated: true
type: note
---

问题：在IP编址中，网络号（网络号）与它能容纳的主机数（容纳的主机数）之间有什么关系？

答案：

**网络号**（网络号）决定了有多少比特用于标识网络与主机，从而直接控制主机容量。

**核心关系：**

如果一个网络的主机部分有 **n 位**：

> **最大主机数 = 2ⁿ − 2**

**−2** 排除了：

- **网络地址**（主机位全为 0）——标识网络本身
- **广播地址**（主机位全为 1）——向网络内所有主机发送

**有类示例：**

| Class | Network Bits | Host Bits (n) | Max Hosts |
| ------- | ------------- | --------------- | ----------- |
| A | 8 | 24 | 2²⁴ − 2 = 16,777,214 |
| B | 16 | 16 | 2¹⁶ − 2 = 65,534 |
| C | 24 | 8 | 2⁸ − 2 = 254 |

**CIDR（无类别）示例：**

`/26` 子网表示 26 位是网络号 → 剩余 **6 位主机位**：

- 2⁶ − 2 = **62 个可用主机**

**关键要点：**

> 网络号越大（位越多），主机空间越小——网络粒度与主机容量之间存在反向权衡。

参考资料：

- [IP Addressing and Subnetting – Cisco](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)
- [Classless Inter-Domain Routing (CIDR) – RFC 4632](https://datatracker.ietf.org/doc/html/rfc4632)
- [IP Address Classes – GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-classful-ip-addressing/)
