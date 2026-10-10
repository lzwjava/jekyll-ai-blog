---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10BASE-T Hub Node Distance
translated: false
type: note
---

**Question:** What is 10BASE-T, and what is the maximum distance between a hub and a node?

**Answer:**

**10BASE-T Overview**

10BASE-T is an early Ethernet standard defined in IEEE 802.3i (1990). The name breaks down as:

| Part | Meaning |
| ------ | --------- |
| **10** | 10 Mbps data rate |
| **BASE** | Baseband signaling |
| **T** | Twisted pair (UTP) cable |

Key characteristics:

- **Topology:** Star (each node connects individually to a central hub)
- **Cable:** Unshielded Twisted Pair (UTP), Cat 3 or higher
- **Connector:** RJ-45
- **Duplex:** Half-duplex (hub-based); full-duplex possible with a switch
- **Signal:** Manchester encoding

---

**Maximum Distance: Hub ↔ Node**

> **100 meters (328 feet)** per segment

This is the maximum cable run from a hub (or switch) port to any single node (PC, printer, etc.). Beyond 100 m, signal attenuation causes errors.

To extend reach, you can cascade hubs — but the **5-4-3 rule** applies to the overall network:

- Max **5** segments
- Connected by **4** repeaters/hubs
- Only **3** segments may have active nodes

---

**References:**

- [IEEE 802.3 Standard Overview – IEEE](https://www.ieee802.org/3/)
- [10BASE-T – Wikipedia](https://en.wikipedia.org/wiki/10BASE-T)
- [Ethernet Cabling Standards – Cisco](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/12006-ethernet-00.html)
