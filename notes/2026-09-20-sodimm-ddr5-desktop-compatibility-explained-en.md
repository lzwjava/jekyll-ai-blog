---
audio: false
generated: true
image: false
lang: en
layout: post
title: SODIMM DDR5 Desktop Compatibility Explained
translated: false
type: note
---

**Question:** Can the Micron DDR5 4800MHz 8GB laptop SO-DIMM (no heatspreader) be used in a desktop PC?

**Answer:** **No, it cannot be used directly in a desktop PC.**

Here's why:

**Form Factor Mismatch — the core issue:**
This Micron DDR5 4800MHz 8GB module is a **SO-DIMM** (Small Outline DIMM) with **262 pins** and dimensions of approximately 68mm × 30mm. Desktop motherboards use standard full-size **DIMM** slots (288 pins, ~133mm long) — a completely different physical connector. This module is specifically classified as compatible with **laptops only**.

The two formats are **physically incompatible** — a SO-DIMM will not fit into a desktop DIMM slot, and the pin counts don't match.

---

**Summary of key differences:**

| Feature | This Module (SO-DIMM) | Desktop (DIMM) |
| --- | --- | --- |
| Form Factor | SO-DIMM | DIMM |
| Pins | 262 | 288 |
| PCB Length | ~68mm | ~133mm |
| Use Case | Laptop / Mini-PC | Desktop motherboard |

---

**Workaround (if you really want to use it):**

There are **SO-DIMM to DIMM adapter cards** sold on the market. However, they are generally **not recommended** because:

- Compatibility is not guaranteed with all motherboards
- They may cause instability
- DDR5 SO-DIMM adapters are rare and niche products

**Bottom line:** If you need memory for a desktop, you should buy a standard DDR5 **DIMM** module (288-pin) instead. The Micron DDR5 4800 8GB SO-DIMM is strictly designed for laptops or compact systems (like Intel NUC) with SO-DIMM slots.

---

**References:**

- [Micron 8GB DDR5 4800 SODIMM 262-Pin specs (A-Tech)](https://atechmemory.com/products/mtc4c10163s1sc48ba1-micron-ram-8gb-1rx16-pc5-38400-sodimm-ddr5-4800-non-ecc-unbuffered-laptop-memory-module)
- [Best DDR5 SO-DIMMs for Laptops — Face of IT](https://www.faceofit.com/best-ddr5-so-dimms-for-laptops/amp)
