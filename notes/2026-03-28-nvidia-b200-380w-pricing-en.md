---
audio: false
generated: true
image: false
lang: en
layout: post
title: Estimated Pricing for NVIDIA B200 380W
translated: false
type: note
---

Question: How much does the NVIDIA Blackwell B200 (380W variant) cost?

Answer: The **NVIDIA B200** with a **380W TDP** is a specific energy-efficient variant of the Blackwell architecture, typically designed for PCIe form factors or power-constrained data center environments. This differs significantly from the flagship **SXM** version, which can draw up to **1,000W**.

### Estimated Pricing for B200 (380W PCIe)
Because NVIDIA sells these primarily through **OEM partners** (like Dell, HPE, and Supermicro), there is no fixed MSRP. However, based on current enterprise listings and market data for 2026, here are the estimated costs:

* **Individual Unit Price:** Generally estimated between **$25,000 and $32,000**. The lower power draw and PCIe interface usually position it at a slightly lower price point than the high-performance 1,000W SXM modules ($35k–$40k).
* **System Integration:** When purchased as part of a 4-GPU or 8-GPU rack-mounted server, the effective cost per card often drops toward the **$25,000** mark due to volume scaling.

### Key Specifications (380W vs. 1,000W)
The 380W variant is optimized for **efficiency** and **air-cooling**, whereas the 1,000W version often requires liquid-cooled infrastructure.

| Feature | B200 (380W PCIe) | B200 (1,000W SXM) |
| :--- | :--- | :--- |
| **Form Factor** | **PCIe 5.0 Dual-Slot** | **SXM5 Module** |
| **Max TDP** | **380W** | **1,000W** |
| **VRAM** | **192GB HBM3e** | **192GB HBM3e** |
| **FP4 Performance** | ~4.5 PFLOPS (Estimated) | **9.0 PFLOPS** |
| **Cooling** | **Air-cooled** (Passive) | **Liquid-cooled** / Advanced Air |

### Why the Price Varies
* **Availability:** While 1,000W units are prioritized for massive "AI Factories," the 380W PCIe cards are more common in **enterprise edge** and **private cloud** setups.
* **Support Packages:** Enterprise prices almost always include a 3-year or 5-year **NVIDIA AI Enterprise** software license, which can add **$2,000–$4,000** to the base hardware cost.

References:
* [NVIDIA B200 Specs & Price | Jarvislabs](https://jarvislabs.ai/gpu/nvidia-b200)
* [How much does an NVIDIA B200 GPU cost? | Northflank](https://northflank.com/blog/how-much-does-an-nvidia-b200-gpu-cost)
* [NVIDIA B200 GPU Price Comparison - GPUs.io](https://gpus.io/en/gpus/b200)

Would you like me to find specific server configurations (like those from Dell or Supermicro) that support the 380W PCIe B200 to see the total system cost?
