---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10 Gigabit Ethernet Full-Duplex Only
translated: false
type: note
---

**Question:** Does 10 Gigabit Ethernet (万兆位以太网) operate in full-duplex or half-duplex mode?

**Answer:**

**10 Gigabit Ethernet supports Full-Duplex (全双工) only.**

| Property | Detail |
| --- | --- |
| **Mode** | Full-Duplex (全双工) **only** |
| **Half-Duplex** | ❌ Not supported |
| **CSMA/CD** | ❌ Not used (no collision detection needed) |
| **Simultaneous TX/RX** | ✅ Send and receive at 10 Gbps at the same time |

---

### Why no Half-Duplex?

- 10GbE was designed **exclusively for switched networks** — every device connects point-to-point to a switch, so there is no shared medium and no collisions.
- **CSMA/CD** (the collision detection mechanism used in half-duplex Ethernet) was **officially removed** from the standard at 10 Gbps.
- This applies to **all** 10GbE variants — fiber (10GBASE-SR/LR/ER) and copper (10GBASE-T/CX4/DAC).

> Note: Half-duplex was already becoming rare at 1GbE (1000BASE-T), and was completely dropped at 10GbE.

---

**References:**

- [10 Gigabit Ethernet – Wikipedia](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet)
- [IEEE 802.3ae Standard Overview](https://standards.ieee.org/ieee/802.3ae/1768/)
