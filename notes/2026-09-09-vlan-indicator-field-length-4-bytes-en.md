---
audio: false
generated: true
image: false
lang: en
layout: post
title: "VLAN Indicator Field Length: 4 Bytes"
translated: false
type: note
---

Question: In a VLAN frame (802.1Q), what is the length of the VLAN indicator field?

Answer:

In an IEEE 802.1Q VLAN-tagged Ethernet frame, the VLAN tag is **4 bytes (32 bits)** total, inserted between the Source MAC address and the EtherType/Length field. It breaks down as:

| Field | Size | Description |
|---|---|---|
| **TPID** (Tag Protocol Identifier) | 16 bits | Always `0x8100` to indicate a VLAN frame |
| **TCI** (Tag Control Information) | 16 bits | Contains PCP (3 bits) + DEI (1 bit) + **VLAN ID (12 bits)** |

The **VLAN ID (VID)** itself is **12 bits**, allowing for **4,096 possible VLANs** (0–4095), though 0 and 4095 are reserved in practice.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        TPID = 0x8100          |PCP|D|        VLAN ID          |
|           (16 bits)           |(3b)|I|       (12 bits)        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        ← 4 bytes total →
```

References:
- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [IEEE 802.1Q Standard](https://standards.ieee.org/ieee/802.1Q/10673/)
