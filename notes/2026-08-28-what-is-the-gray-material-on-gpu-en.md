---
audio: false
generated: true
image: false
lang: en
layout: post
title: What Is the Gray Material on GPU
translated: false
type: note
---

**Question:** What is the gray material on top of a GPU die (like a Quadro 410) when you remove the fan, and does it allow heat to flow out easily?

**Answer:** That gray material is **thermal paste** (also called thermal compound or thermal grease). Here's a breakdown of what it is and how it works:

**What it is:**
It's a thermally conductive paste — typically a silicone-based compound filled with fine metallic or ceramic particles (zinc oxide, silver, or similar). On a Quadro 410 and most GPUs in that era, NVIDIA used a generic gray silicone grease.

**What it does:**
The GPU die and the heatsink surface are both microscopically rough and uneven. If you pressed them together directly, tiny air pockets would form in between — and air is a terrible conductor of heat. The thermal paste fills those microscopic gaps, creating a continuous conductive bridge from the die to the heatsink.

**Does heat flow out easily through it?**
Thermal paste *does* allow heat to flow out, but it's not a great conductor on its own — it's just *far better than air*. A few key points:

- Thermal paste has a thermal conductivity of roughly **3–8 W/m·K** for typical gray silicone compounds (premium silver pastes can reach ~9–10 W/m·K).
- Copper, for comparison, is around **400 W/m·K** — so paste is still a weak link, which is why it's applied in a **very thin layer**. Thinner = better.
- Old, dried-out paste (common on a used Quadro 410) becomes cracked and less effective, causing temperatures to rise noticeably.
- Without any paste, the GPU can overheat quickly due to those air gaps.

**In short:** It's doing its job to facilitate heat flow, but it works best when it's fresh and applied thinly. If the paste on your Quadro 410 looks dried or crumbly, replacing it with fresh paste (even a cheap one) will meaningfully lower temperatures.**References:**
- [Thermal Interface Materials Explained – Thermal Grizzly](https://www.thermal-grizzly.com/en/thermal-interface-materials)
- [Why Thermal Paste Matters – Linus Tech Tips](https://linustechtips.com/topic/thermal-paste-importance)
- [NVIDIA Quadro 410 Specs & Cooling – TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/quadro-410.c1723)
