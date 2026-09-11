---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Dual Power Supplies: Possible but Unnecessary"
translated: false
type: note
---

**Question:** Can a secondary/additional power supply be used to power a dedicated GPU (like an RTX 3060) when the main PSU is only 400W?

**Answer:**

Yes, technically it's possible, but it comes with significant caveats:

**Why you might need to:**
- An RTX 3060 requires around **170W TDP**, and Nvidia recommends a **550W system PSU** — your 400W unit is borderline or insufficient for the whole system.

**How a dual-PSU setup works:**
- You can use a second PSU dedicated to the GPU using an **"Add2PSU" or dual-PSU adapter**, which synchronizes the power-on signal of both units so they start simultaneously.
- The GPU's PCIe power connectors (8-pin or 6+2-pin) plug into the second PSU, while the motherboard, CPU, and storage stay on the primary 400W unit.

**Practical considerations:**

| Factor | Detail |
|---|---|
| **Cost** | A decent secondary PSU + Add2PSU adapter adds cost — often cheaper to just upgrade to a 550W+ unit |
| **Complexity** | More cables, more points of failure, takes extra space |
| **Stability** | Ground loops and startup sync issues can cause instability |
| **Safety** | Mismatched PSUs or improper setup can damage components |
| **Efficiency** | Running two PSUs is less efficient than one properly-sized unit |

**Recommendation:**

The simplest and safest solution is to **replace the 400W PSU with a single 550–650W unit** from a reputable brand (Seasonic, Corsair, EVGA, be quiet!). A decent 650W 80+ Bronze PSU costs roughly $50–80 and eliminates all dual-PSU complexity. The dual-PSU approach is mainly used in mining rigs or very specific modding scenarios, not typical desktop builds.

---

**References:**
- [RTX 3060 Specs & Power Requirements – Nvidia](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/)
- [How to Use Two Power Supplies Together – Lifewire](https://www.lifewire.com/connect-two-power-supplies-together-4692260)
- [PSU Calculator – OuterVision](https://outervision.com/power-supply-calculator)
