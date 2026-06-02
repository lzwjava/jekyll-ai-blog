---
audio: false
generated: true
image: false
lang: en
layout: post
title: ICMP Inside IP Datagrams Explained
translated: false
type: note
---

Question: In what is an ICMP message encapsulated for transmission?

Answer:

ICMP (Internet Control Message Protocol) messages are encapsulated within **IP datagrams** (or IP packets) for transmission.

Although ICMP is considered a network layer protocol (Layer 3) and is used to send error messages and operational information about IP packet processing, it does not have its own direct access to the data link layer. Instead, an ICMP message forms the payload (data portion) of an IP datagram. The IP header is then added to this payload, specifying the source and destination IP addresses, before the entire unit is passed down to the data link layer for framing and transmission.

Key points:

- **Protocol Number**: In the IP header, the "Protocol" field is set to **1** to indicate that the payload is an ICMP message.
- **Relationship**: ICMP is often described as an integral part of IP, but logically it sits "on top" of IP because its messages are carried inside IP packets.
- **Structure**: `[ IP Header | ICMP Header | ICMP Data ]`

Therefore, the blank in your sentence should be filled with **IP data报** (IP datagram).

References:
