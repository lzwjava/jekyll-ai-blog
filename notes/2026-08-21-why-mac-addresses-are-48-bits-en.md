---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why MAC Addresses Are 48 Bits
translated: false
type: note
---

Question: Why are both the source and destination MAC addresses in the IEEE 802.3 MAC frame structure 48 bits (6 bytes)?

Answer:

In the IEEE 802.3 (Ethernet) MAC frame structure, both the **Destination Address (DA)** and **Source Address (SA)** are **48 bits (6 bytes)** each. Here's why:

**MAC Address Standard**
IEEE standardized MAC addresses as 48-bit values. This is defined in IEEE 802 and applies universally across Ethernet, Wi-Fi, Bluetooth, etc.

**Structure of a 48-bit MAC Address**

```
| OUI (24 bits)  | NIC-specific (24 bits) |
  Organizationally    Device identifier
  Unique Identifier
```

- First 3 bytes → assigned to manufacturers by IEEE
- Last 3 bytes → assigned by the manufacturer to each device

**Why not the other options?**

| Option | Bits | Reason it's wrong |
| -------- | ------ | ------------------- |
| A – 16 bit | 2 bytes | Too small; only ~65,536 unique addresses |
| **C – 48 bit** | **6 bytes** | **Correct — IEEE 802 standard** |
| B – 32 bit | 4 bytes | That's IPv4 address size, not MAC |
| D – 96 bit | 12 bytes | That would be two MAC addresses combined |

**Memory tip:** A MAC address is commonly written as 6 pairs of hex digits, e.g. `AA:BB:CC:DD:EE:FF` — 6 bytes = 48 bits.

References:

- [IEEE 802.3 Ethernet Standard](https://standards.ieee.org/ieee/802.3/7071/)
- [MAC Address – Wikipedia](https://en.wikipedia.org/wiki/MAC_address)
