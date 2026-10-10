---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1000BASE-T Transfer Medium
translated: false
type: note
---

**Question:** What is the transfer medium used by 1000BASE-T?

**Answer:**

**1000BASE-T** (defined in IEEE 802.3ab) uses **twisted pair copper cabling** as its transfer medium — specifically:

| Property | Detail |
|---|---|
| **Medium** | Unshielded Twisted Pair (UTP) copper wire |
| **Minimum cable grade** | Cat 5e (Category 5e) or higher (Cat 6, Cat 6a also work) |
| **Wire pairs used** | All **4 pairs** (8 wires) simultaneously |
| **Max segment length** | 100 meters (328 ft) |
| **Speed** | 1 Gbps (Gigabit Ethernet) |
| **Signaling** | Full-duplex, PAM-5 encoding on each pair |

Unlike earlier standards (e.g., 100BASE-TX uses only 2 pairs), 1000BASE-T leverages all 4 wire pairs **bidirectionally at the same time**, which is how it achieves gigabit speed over ordinary copper cabling.

**References:**
- [IEEE 802.3ab – Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.3ab)
- [1000BASE-T – Ethernet Alliance](https://ethernettechnology.net/gigabit-ethernet/)