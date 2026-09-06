---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1000BASE-T 100m Cat5e Required
translated: false
type: note
---

**Question:** What is the maximum effective transmission distance for 1000BASE-T, and does it use Cat 5 or Cat 5e UTP cable?

**Answer:**

**Maximum Distance: 100 meters (328 feet)**

The maximum cable length for 1000BASE-T is **100 meters (328 feet)** when using Category 5e or better copper cabling. This distance includes the horizontal cable run *plus* patch cords at both ends.

---

**Cable Category — You're close, but Cat 5e is the real answer:**

You mentioned Cat 5 or Cat 5e — the correct minimum is **Cat 5e** (not plain Cat 5).

- While 1000BASE-T was *designed* for Category 5e cable, it *may* work with high-quality Category 5 cable under optimal conditions. However, Category 5 cable does not provide the performance margins necessary for reliable gigabit operation, particularly over longer distances or in environments with electromagnetic interference. For guaranteed performance, **Cat 5e or better is strongly recommended**.

- The minimum cable typically used for 1000BASE-T is **Cat 5e**, and unlike 100 Mbps Ethernet which uses only 2 pairs, **1000BASE-T requires all 4 pairs** inside the twisted pair cable.

- 1000BASE-T can also run on Cat 6, Cat 6A, Cat 7, Cat 7A, and Cat 8 — all at the same 100-meter limit.

---

**Encoding:** Each of the 4 pairs carries 250 Mbps using **PAM-5** (Pulse Amplitude Modulation with 5 levels), totaling 1 Gbps full-duplex.

---

**References:**

- [1000BASE-T Overview – Ctools.org](https://ctools.org/detailed-overview-of-the-1000base-t-gigabit-ethernet-standard-on-copper-cabling/)
- [Wiring for 1000BASE-T – Infinity Cable Products](https://infinity-cable-products.com/blogs/performance/how-many-cable-pairs-are-needed-for-1000base-t-transmission)
- [Ethernet Standards – Professor Messer](https://www.professormesser.com/professor-messer-archives/n10-007/ethernet-standards-3/)
