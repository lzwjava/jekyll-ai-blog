---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 4000 Power Requirements
translated: false
type: note
---

**Question:** How many watts does the Quadro 4000 power cable need to supply?

**Answer:**

The NVIDIA Quadro 4000 has a **maximum power draw of 80W** total:

| Source | Power |
| --- | --- |
| PCIe slot (motherboard) | up to 75W |
| 6-pin PCIe cable | up to 75W additional |
| **Card TDP (total)** | **80W max** |

So your PSU only needs to supply a modest amount through the 6-pin cable. A **standard 6-pin PCIe connector is rated for 75W**, which is more than enough for this card.

**Key takeaway:** Any modern ATX PSU with a 6-pin PCIe connector can handle this card easily. The Quadro 4000 is a relatively low-power workstation card — the minimum recommended power supply is **300W**, so most systems will have no problem.

**References:**

- [NVIDIA Quadro Power Guidelines (PNY)](https://www.pny.com/file%20library/company/support/product%20brochures/nvidia%20quadro/quadro-power-guidelines.pdf)
- [Quadro K4000 power info – Ten Forums](https://www.tenforums.com/graphic-cards/211663-inserted-old-pc-nvidia-quadro-k4000-but-prompts-pow.html)
