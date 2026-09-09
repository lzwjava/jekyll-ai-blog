---
audio: false
generated: true
image: false
lang: en
layout: post
title: 0x0600 EtherType Threshold
translated: false
type: note
---

**Question:** What does 0x0600 (0x600) mean in the context of IEEE 802 (Ethernet)?

**Answer:**

`0x0600` (decimal 1536) is not itself an assigned EtherType value — rather, it is the **boundary threshold** that distinguishes EtherType frames from length-based frames in Ethernet.

Here's what it means:

**The Threshold Rule:**
The unifying standard IEEE 802.3x-1997 requires that EtherType values be greater than or equal to 1536 (0x0600). That value was chosen because the maximum length (MTU) of the data field of an Ethernet 802.3 frame is 1500 bytes (0x05DC). Thus, values of 1500 and below indicate that the field represents the **size of the payload**, while values of 1536 and above indicate that the field represents an **EtherType** (protocol identifier). The interpretation of values 1501–1535 is undefined.

**Why this matters:**

- **≤ 0x05DC (1500)** → The field is a **length** field (IEEE 802.3 framing)
- **≥ 0x0600 (1536)** → The field is an **EtherType** (protocol identifier, Ethernet II framing)
- **0x0601–0x05FF** → Undefined / reserved gap

**Common EtherType examples above 0x0600:**

| EtherType | Protocol |
| ----------- | ---------- |
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN (802.1Q) |

So in short, `0x0600` is the **minimum boundary value** for valid EtherTypes — it's a design marker, not a protocol assignment itself.

**References:**

- [EtherType – Wikipedia](https://en.wikipedia.org/wiki/EtherType)
- [RFC 7042 – IEEE 802 Parameters (IETF)](https://datatracker.ietf.org/doc/rfc7042/)
- [EtherType – Networx Security](https://www.networxsecurity.org/members-area/glossary/e/ethertype.html)
