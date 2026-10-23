---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv4总长度字段大小
translated: true
type: note
---

问题：IPv4 头部中 "Total Length" 字段占用多少 bits？

答案：IPv4 头部中的 **Total Length** 字段占用 **16 bits**（2 bytes）。

它表示 IP 数据报（header + payload）的总大小（以 bytes 为单位）。由于它宽度为 16 bits，最大值为 2¹⁶ − 1 = **65,535 bytes**。

以下是相关 IPv4 头部字段及其大小的快速参考：

| 字段 | 大小 |
|---|---|
| Version | 4 bits |
| IHL (Header Length) | 4 bits |
| DSCP / ECN | 8 bits |
| **Total Length** | **16 bits** |
| Identification | 16 bits |
| Flags + Fragment Offset | 16 bits |
| TTL | 8 bits |
| Protocol | 8 bits |
| Header Checksum | 16 bits |
| Source Address | 32 bits |
| Destination Address | 32 bits |

参考：
- [RFC 791 – Internet Protocol (IETF)](https://datatracker.ietf.org/doc/html/rfc791)
- [IPv4 Header – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Packet_structure)