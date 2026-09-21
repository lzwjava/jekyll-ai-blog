---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet MAC Address Length
translated: false
type: note
---

Question: In an Ethernet MAC frame, are the source and target addresses both 48 bits?

Answer: **Yes — for standard Ethernet, both are 48-bit (6-byte) MAC addresses.**

```text
Ethernet II frame
┌──────────────┬──────────────┬────────────┬───────────────┐
│ Dest MAC     │ Source MAC   │ EtherType  │ Payload ...   │
│ 48 bits      │ 48 bits      │ 16 bits    │ 46–1500 bytes │
└──────────────┴──────────────┴────────────┴───────────────┘
     6 bytes        6 bytes       2 bytes
```

Example:

```text
dst = ff:ff:ff:ff:ff:ff    # broadcast
src = 3c:22:fb:12:34:56    # unicast
```

A MAC address is therefore:

```text
48 bits = 6 bytes = 12 hexadecimal digits
```

One subtlety: **48-bit is the normal Ethernet MAC address size, but not every MAC-layer protocol/addressing scheme is necessarily 48-bit.** Ethernet specifically uses 48-bit MAC addresses in the common case.

References:

* [IEEE 802.3 Ethernet](https://standards.ieee.org/ieee/802.3/10422/)
* [RFC 7042 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802](https://www.rfc-editor.org/rfc/rfc7042)

I can also walk through an actual Ethernet frame byte-by-byte, including where the preamble, FCS, EtherType, and IP/TCP headers sit.
