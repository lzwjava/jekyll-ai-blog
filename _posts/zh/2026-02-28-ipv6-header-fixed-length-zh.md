---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv6 头部固定长度详解
translated: true
type: note
---

问题：What is the length of the basic header of an IPv6 datagram?

答案： 

正确答案是 **C. 40B**。

**解释：**

在 IPv6 中，与 IPv4 相比，header 结构进行了重大重新设计，以提高效率、简化处理并支持更大的寻址空间。

**IPv6 base header**（也称为 fixed header 或 basic header）具有 **固定的 40 bytes**（320 bits）长度。此长度是恒定的，并且 **不会** 变化。

关于 IPv6 base header 的关键点：
- 始终精确为 **40 bytes** 长
- 只包含每个数据包所需的字段
- **不** 在主头部中包含 options（与 IPv4 不同）
- 任何附加信息都放置在紧随 base header 的 **extension headers** 中（这些是可选的，并且长度可变）

IPv6 base header 的结构（总计 40 bytes）：
- Version (4 bits)
- Traffic Class (8 bits)
- Flow Label (20 bits)
- Payload Length (16 bits)
- Next Header (8 bits)
- Hop Limit (8 bits)
- Source Address (128 bits = 16 bytes)
- Destination Address (128 bits = 16 bytes)

总计：4 + 8 + 20 + 16 + 8 + 8 + 128 + 128 = **320 bits = 40 bytes**

**与 IPv4 的比较**：
- IPv4 header 通常为 **20 bytes**（不含 options），但如果存在 options 则可能更长。
- IPv6 使用固定的 **40-byte** base header —— 比基本的 IPv4 长，但由于长度永不变更，因此更简单且处理更快。

因此，IPv6 basic header 的长度是 **40 bytes**。

正确选项：**C**

参考文献：  

- 无（标准网络知识 / RFC 8200 - Internet Protocol, Version 6 (IPv6) Specification）