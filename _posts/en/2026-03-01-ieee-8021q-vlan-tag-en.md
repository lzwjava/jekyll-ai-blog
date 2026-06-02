---
audio: false
generated: true
image: false
lang: en
layout: post
title: IEEE 802.1Q VLAN Tag Explained
translated: false
type: note
---

Question: According to the IEEE 802.1Q standard, which defines the Ethernet frame format in a virtual LAN environment, a 4-byte field is used to indicate which virtual LAN the host sending the frame belongs to. What is the name of this field?

Answer:

The correct answer is **VLAN标记** (VLAN Tag) or **Tag**.

In the IEEE 802.1Q standard, an additional 4-byte field called the **VLAN Tag** (also commonly referred to as the 802.1Q tag or simply "Tag") is inserted into the Ethernet frame. This tag identifies the Virtual Local Area Network (VLAN) to which the frame belongs.

The structure of the VLAN Tag is as follows:

- **TPID** (Tag Protocol Identifier): 2 bytes, fixed value 0x8100
- **TCI** (Tag Control Information): 2 bytes, which contains:
  - Priority Code Point (PCP): 3 bits
  - Drop Eligible Indicator (DEI): 1 bit (formerly CFI)
  - VLAN Identifier (VID): 12 bits (the actual VLAN number, 0–4095)

This 4-byte VLAN Tag field is what allows switches to distinguish and separate traffic from different VLANs on the same physical link (trunk link).

Therefore, the 4-byte field used to indicate which VLAN the sending host belongs to is called the **VLAN Tag** (or VLAN标记 / Tag in Chinese).

References:

- None (standard networking knowledge based on IEEE 802.1Q specification)
