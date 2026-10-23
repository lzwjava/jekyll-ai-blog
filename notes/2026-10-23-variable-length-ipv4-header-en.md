---
audio: false
generated: true
image: false
lang: en
layout: post
title: Variable Length IPv4 Header
translated: false
type: note
---

**Question:** In an IPv4 datagram, what is the length of the header (首部)?

**Answer:**

An IPv4 header has a **variable length**, determined by the **IHL (Internet Header Length)** field — a 4-bit field that specifies the header size in units of **32-bit (4-byte) words**.

| Parameter | Value |
| --- | --- |
| Minimum header length | **20 bytes** (160 bits) — no options |
| Maximum header length | **60 bytes** (480 bits) — with options |
| IHL field size | 4 bits → values 5–15 |
| Unit | 32-bit words (4 bytes each) |

**Key details:**

- **IHL = 5** → 5 × 4 = **20 bytes** (the most common case, no options)
- **IHL = 15** → 15 × 4 = **60 bytes** (maximum, with options fully filled)
- The header **must always be a multiple of 4 bytes**; padding is added if needed.

The fixed part of the header is always 20 bytes and includes fields like Version, IHL, TTL, Protocol, Source/Destination IP, etc. The optional part (0–40 bytes) covers things like timestamps, routing options, and security.

---

**References:**

- [RFC 791 – Internet Protocol (IPv4)](https://www.rfc-editor.org/rfc/rfc791)
- [IPv4 – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Header)
