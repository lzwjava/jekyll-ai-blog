---
audio: false
generated: true
image: false
lang: en
layout: post
title: UDP Checksum Field
translated: false
type: note
---

Question: What field does UDP use to ensure data correctness?

Answer:

UDP uses the **Checksum** field to ensure data correctness.

- It is a 16-bit field in the UDP header.
- It covers the UDP header, the UDP data (payload), and a pseudo-header derived from the IP header (source/destination IP, protocol, UDP length).
- The sender computes the checksum and fills the field; the receiver recomputes it and compares — if they don't match, the packet is discarded.
- In IPv4, the checksum is **optional** (a value of `0x0000` means it was not computed); in IPv6, it is **mandatory**.

UDP header structure for reference:

| Field | Size |
|---|---|
| Source Port | 16 bits |
| Destination Port | 16 bits |
| Length | 16 bits |
| **Checksum** | **16 bits** |

> Note: UDP provides only basic error *detection* (not correction). If a packet fails the checksum, it is simply dropped — UDP does not retransmit.

References:
- [RFC 768 – User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [UDP – MDN Web Docs Glossary](https://developer.mozilla.org/en-US/docs/Glossary/UDP)
