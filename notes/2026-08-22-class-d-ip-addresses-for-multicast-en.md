---
audio: false
generated: true
image: false
lang: en
layout: post
title: Class D IP Addresses for Multicast
translated: false
type: note
---

Question: What are Class D IP addresses (highest 4 bits = 1110) used for?

Answer: Class D IP addresses, whose highest 4 bits are **1110**, are reserved for **IP Multicasting**.

- The address range is **224.0.0.0 – 239.255.255.255**.
- Instead of sending a packet to a single host (unicast) or all hosts (broadcast), multicast allows a single packet to be delivered simultaneously to a **group of interested receivers**.
- Typical use cases include video conferencing, live streaming, IPTV, and routing protocol updates (e.g., OSPF uses 224.0.0.5).
- Hosts join a multicast group using the **IGMP (Internet Group Management Protocol)**.

| Class | Highest bits | Range | Purpose |
| ------- | ------------- | ------- | --------- |
| A | 0 | 0–127 | Unicast (large networks) |
| B | 10 | 128–191 | Unicast (medium networks) |
| C | 110 | 192–223 | Unicast (small networks) |
| **D** | **1110** | **224–239** | **Multicast** |
| E | 1111 | 240–255 | Reserved/Experimental |

References:

- [IP Multicast - Wikipedia](https://en.wikipedia.org/wiki/IP_multicast)
- [RFC 1112 – Host Extensions for IP Multicasting](https://datatracker.ietf.org/doc/html/rfc1112)
