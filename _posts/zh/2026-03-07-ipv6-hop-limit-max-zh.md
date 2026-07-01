---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv6 跳数限制最大值
translated: true
type: note
---

问题：在 IPv6 中，“Hop Limit” 字段的最大值是多少？

答案：

## IPv6 Hop Limit 字段

正确答案是 **C: 255**。

### 解释

IPv6 中的 **Hop Limit** 字段是 IPv6 头部中的一个 8 位字段。以下是关键细节：

| 属性 | 值 |
| --- | --- |
| 字段名称 | Hop Limit |
| 字段大小 | **8 bits (1 byte)** |
| 最大值 | **255** |
| 最小值 | 0 |

### 为什么是 255？

由于 Hop Limit 字段是 **8 bits** 长，它可以存储从 `0` 到 `2^8 - 1 = 255` 的值。

- 每次 IPv6 数据包通过一个 **router (hop)** 时，路由器会将此值 **减 1**。
- 当值达到 **0** 时，数据包被 **丢弃**，并向源发送 ICMPv6 “Time Exceeded” 消息。
- 此机制 **防止数据包在互联网上无限循环**。

### 与 IPv4 的比较

| 特性 | IPv4 | IPv6 |
| --- | --- | --- |
| 字段名称 | TTL (Time To Live) | Hop Limit |
| 大小 | 8 bits | 8 bits |
| 最大值 | 255 | 255 |
| 目的 | 防止无限循环 | 防止无限循环 |

IPv6 Hop Limit 在功能上等同于 IPv4 中的 **TTL 字段**，但更名为更好地反映其实际行为——计算 **hops (router traversals)** 而非时间。

### 其他选项为什么错误

- **A (1024)**：不可能——8 bits 无法存储超过 255 的值。
- **B (256)**：不可能——8 bits 最大值为 255 (0–255)，不是 256。
- **D (254)**：接近，但 254 不是 **最大** 值；255 仍然有效且可实现。
