---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv4 Protocol Field Bit Size
translated: false
type: note
---

Question: In an IPv4 datagram, how many bits does the **Protocol** field occupy?

Answer: **8 bits (1 byte).**

In the IPv4 header:

```text
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |    DSCP/ECN  |        Total Length           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   TTL   |  Protocol  |             Header Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

The **Protocol** field is exactly **8 bits**.

It identifies the upper-layer protocol carried inside the IP payload:

```text
Protocol = 6   → TCP
Protocol = 17  → UDP
Protocol = 1   → ICMP
```

So the basic encapsulation is:

```text
Ethernet
   └── IPv4 datagram
         ├── IPv4 header
         │     └── Protocol: 8 bits
         └── Payload
               └── TCP / UDP / ICMP ...
```

References:

* RFC 791 — Internet Protocol (IPv4) specification
* IANA Protocol Numbers registry

I can also walk through the entire **20-byte minimum IPv4 header field-by-field**, including the exact bit widths.
