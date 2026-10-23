---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv4 Identification Field for Fragmentation
translated: false
type: note
---

Question: What is the "标识字段" (Identification field) in an IP datagram?

Answer:

The **Identification field** (标识字段) is a **16-bit field** in the IPv4 header, used primarily for **IP fragmentation and reassembly**.

---

### Role & Purpose

When an IP datagram is too large to fit within the **MTU (Maximum Transmission Unit)** of a network link, it gets **fragmented** into smaller pieces. The Identification field serves as a **shared tag** that ties all fragments of the same original datagram together so the destination host can reassemble them correctly.

---

### Key Characteristics

| Property | Detail |
| --- | --- |
| Size | 16 bits |
| Position in header | Bytes 4–5 of the IPv4 header |
| Assigned by | The **sending host** (typically an incrementing counter) |
| Scope | Unique per (source IP, destination IP, protocol) pair — within a reasonable time window |

---

### How It Works (Fragmentation Example)

```
Original datagram (4000 bytes, ID = 1234)
         ↓  fragmented at router
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ ID=1234  Frag 1 │  │ ID=1234  Frag 2 │  │ ID=1234  Frag 3 │
│ Offset=0        │  │ Offset=185      │  │ Offset=370      │
│ MF=1            │  │ MF=1            │  │ MF=0 (last)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         ↓  destination reassembles using ID + Fragment Offset + MF flag
         Original datagram (4000 bytes, ID = 1234)
```

All three fragments share the **same ID (1234)**, so the receiver knows they belong together.

---

### Related Header Fields (work together with ID)

- **Fragment Offset** (13 bits) — position of this fragment in the original datagram
- **More Fragments (MF) flag** (1 bit) — `1` = more fragments follow; `0` = this is the last one
- **Don't Fragment (DF) flag** (1 bit) — if set, the datagram must NOT be fragmented; if it's too big, it's dropped and an ICMP error is returned

---

### Notes

- If **DF=1**, the Identification field is technically unused for fragmentation, but it's still present in the header.
- In **IPv6**, fragmentation by routers is eliminated; fragmentation is handled only by the source host using an **extension header**, and the identification concept is moved there.
- The 16-bit space (65,536 values) can theoretically wrap around on high-speed links, which is a known limitation ([RFC 6864](https://datatracker.ietf.org/doc/html/rfc6864) discusses this).

References:

- [RFC 791 – Internet Protocol (IPv4 specification)](https://datatracker.ietf.org/doc/html/rfc791)
- [RFC 6864 – Updated Specification of the IPv4 ID Field](https://datatracker.ietf.org/doc/html/rfc6864)
