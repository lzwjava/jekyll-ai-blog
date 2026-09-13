---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Bits and Host Capacity
translated: false
type: note
---

Question: In IP addressing, what is the relationship between the network number (网络号) and the number of hosts it can accommodate (容纳的主机数)?

Answer:

The **network number** (网络号) determines how many bits are reserved for identifying the network vs. hosts, which directly controls the host capacity.

**Core relationship:**

If a network has **n bits** for the host portion:

> **Max hosts = 2ⁿ − 2**

The **−2** accounts for:

- **Network address** (all host bits = 0) — identifies the network itself
- **Broadcast address** (all host bits = 1) — sends to all hosts on the network

**Classful examples:**

| Class | Network Bits | Host Bits (n) | Max Hosts |
| ------- | ------------- | --------------- | ----------- |
| A | 8 | 24 | 2²⁴ − 2 = 16,777,214 |
| B | 16 | 16 | 2¹⁶ − 2 = 65,534 |
| C | 24 | 8 | 2⁸ − 2 = 254 |

**CIDR (classless) example:**

A `/26` subnet means 26 bits are the network number → **6 host bits** remain:

- 2⁶ − 2 = **62 usable hosts**

**Key insight:**

> The larger the network number (more bits), the smaller the host space — there's an inverse tradeoff between network granularity and host capacity.

References:

- [IP Addressing and Subnetting – Cisco](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)
- [Classless Inter-Domain Routing (CIDR) – RFC 4632](https://datatracker.ietf.org/doc/html/rfc4632)
- [IP Address Classes – GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-classful-ip-addressing/)
