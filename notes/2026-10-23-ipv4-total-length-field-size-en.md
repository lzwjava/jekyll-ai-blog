---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv4 Total Length Field Size
translated: false
type: note
---

Question: How many bits does the "Total Length" field occupy in an IPv4 header?

Answer: The **Total Length** field in an IPv4 header occupies **16 bits** (2 bytes).

It indicates the total size of the IP datagram (header + payload) in bytes. Since it is 16 bits wide, the maximum value is 2¹⁶ − 1 = **65,535 bytes**.

Here is a quick reference of the relevant IPv4 header fields and their sizes:

| Field | Size |
| --- | --- |
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

References:

- [RFC 791 – Internet Protocol (IETF)](https://datatracker.ietf.org/doc/html/rfc791)
- [IPv4 Header – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Packet_structure)
