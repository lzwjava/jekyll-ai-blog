---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv6 Header Fixed Length Explained
translated: false
type: note
---

Question: What is the length of the basic header of an IPv6 datagram?

Answer: 

The correct answer is **C. 40B**.

**Explanation:**

In IPv6, the header structure was significantly redesigned compared to IPv4 to improve efficiency, simplify processing, and support much larger addressing.

The **IPv6 base header** (also called the fixed header or basic header) has a **fixed length of 40 bytes** (320 bits). This length is constant and does **not** vary.

Key points about the IPv6 base header:
- Always exactly **40 bytes** long
- Contains only the fields that are needed in every packet
- Does **not** include options in the main header (unlike IPv4)
- Any additional information is placed in **extension headers** that follow the base header (these are optional and variable in length)

Structure of the IPv6 base header (40 bytes total):
- Version (4 bits)
- Traffic Class (8 bits)
- Flow Label (20 bits)
- Payload Length (16 bits)
- Next Header (8 bits)
- Hop Limit (8 bits)
- Source Address (128 bits = 16 bytes)
- Destination Address (128 bits = 16 bytes)

Total: 4 + 8 + 20 + 16 + 8 + 8 + 128 + 128 = **320 bits = 40 bytes**

**Comparison with IPv4**:
- IPv4 header is typically **20 bytes** (without options), but can be longer if options are present.
- IPv6 uses a fixed **40-byte** base header — longer than basic IPv4, but simpler and faster to process because the length never changes.

Therefore, the length of the IPv6 basic header is **40 bytes**.

Correct choice: **C**

References:  

- None (standard networking knowledge / RFC 8200 - Internet Protocol, Version 6 (IPv6) Specification)