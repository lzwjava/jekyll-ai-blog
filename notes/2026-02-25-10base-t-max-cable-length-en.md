---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10BASE-T Maximum Cable Length Explained
translated: false
type: note
---

Question: According to the 10BASE-T Ethernet technical specification, what is the maximum distance between a HUB and a network interface card (NIC)?

A. 20m
B. 50m
C. 100m
D. 200m

Answer:

**C. 100m**

**Explanation:**

The 10BASE-T standard (defined in IEEE 802.3i-1990) is the 10 Mbps Ethernet specification that uses unshielded twisted-pair (UTP) cabling — typically Category 3 or better — and operates in a physical star topology with a hub (or repeater) at the center.

Key technical parameters of 10BASE-T include:

- Maximum cable length between the hub (repeater) and the network interface card (DTE): **100 meters**
- Uses RJ-45 connectors
- Two pairs of the four pairs in the cable are used (one for transmit, one for receive)
- The 100-meter limit includes patch cords and is the total allowed length of the horizontal cabling segment

This 100-meter maximum segment length is a fundamental rule in 10BASE-T and has been consistently documented in both the original IEEE 802.3 standard and all subsequent references.

Therefore, the correct answer is **C. 100m**.

The other options are incorrect because:
- 20m and 50m are far below the standard allowance
- 200m exceeds the specification and would cause excessive signal attenuation and timing problems

References:

- IEEE 802.3-1990 standard (10BASE-T clause)
- [https://standards.ieee.org/ieee/802.3/1990/](https://standards.ieee.org/ieee/802.3/1990/)
