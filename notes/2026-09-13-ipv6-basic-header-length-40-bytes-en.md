---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv6 Basic Header Length 40 Bytes
translated: false
type: note
---

Question: What is the length of the IPv6 basic header (基本首部)?

Answer: The IPv6 basic header (基本首部) has a **fixed length of 40 bytes (320 bits)**.

Unlike IPv4, which has a variable-length header, IPv6 uses a fixed-size basic header, making processing more efficient for routers.

The 40-byte header contains these fields:

| Field | Size |
|---|---|
| Version | 4 bits |
| Traffic Class | 8 bits |
| Flow Label | 20 bits |
| Payload Length | 16 bits |
| Next Header | 8 bits |
| Hop Limit | 8 bits |
| Source Address | 128 bits |
| Destination Address | 128 bits |
| **Total** | **320 bits = 40 bytes** |

References:
- [RFC 8200 – Internet Protocol, Version 6 (IPv6) Specification](https://datatracker.ietf.org/doc/html/rfc8200#section-3)
- [IPv6 – Wikipedia](https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header)
