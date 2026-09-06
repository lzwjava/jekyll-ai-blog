---
audio: false
generated: true
image: false
lang: en
layout: post
title: 802.1Q VLAN Tagging Explained
translated: false
type: note
---

Question: What does 802.1Q mean in the context of VLANs?

Answer:

**IEEE 802.1Q** is the networking standard that defines how **VLAN tagging** works on Ethernet networks. It's the mechanism that allows a single physical network link to carry traffic from multiple VLANs simultaneously.

---

**How it works:**

802.1Q inserts a **4-byte (32-bit) tag** into the Ethernet frame header between the Source MAC address and the EtherType field. This tag contains:

| Field | Size | Description |
| --- | --- | --- |
| TPID | 16 bits | Tag Protocol ID — always `0x8100` to identify it as an 802.1Q frame |
| PCP | 3 bits | Priority Code Point — for QoS/traffic prioritization |
| DEI | 1 bit | Drop Eligible Indicator — marks frames that can be dropped under congestion |
| VID | 12 bits | **VLAN ID** — identifies which VLAN the frame belongs to (0–4095) |

---

**Key concepts:**

- **VLAN ID range:** 0–4095 (12 bits), though 0 and 4095 are reserved, giving **4094 usable VLANs**
- **Trunk ports:** Links between switches carry tagged frames so both ends know which VLAN a frame belongs to
- **Access ports:** End devices (PCs, servers) typically don't see the tag — the switch adds/removes it automatically
- **Native VLAN:** One VLAN per trunk can be designated "native," meaning its frames are sent **untagged**

---

**In short:** 802.1Q is the universal standard (defined by IEEE) that makes VLANs interoperable across different vendors' switches by embedding VLAN membership directly inside each Ethernet frame.

References:

- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [VLAN Tagging Explained - Cisco](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/layer2/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_Layer_2_Switching_Configuration_Guide/b_Cisco_Nexus_9000_Series_NX-OS_Layer_2_Switching_Configuration_Guide_chapter_0100.html)
- [IEEE 802.1Q Standard Overview](https://standards.ieee.org/ieee/802.1Q/10323/)
