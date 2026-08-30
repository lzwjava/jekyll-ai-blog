---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU Scaling: Prospects and Limits"
translated: false
type: note
---

**Question:** Can GPU performance continue to scale upward, and what are the limits?

**Answer:**

Yes — but scaling is getting harder, more expensive, and increasingly multi-dimensional. Here's the full picture:

---

**🟢 What's still scaling: Nvidia's roadmap through 2028**

Nvidia has shifted from a 2-year to a **1-year release cadence**, with each generation targeting roughly a 2× performance jump:

| Year | Platform | Key GPU | FP4 Compute |
| --- | --- | --- | --- |
| 2025 | Blackwell Ultra | B300 | ~20 PFLOPS |
| 2026 | Vera Rubin | R100 | ~50 PFLOPS |
| 2027 | Rubin Ultra | R300 | ~100 PFLOPS (est.) |
| 2028 | Feynman | — | TBD |

The Vera Rubin platform delivers 50 petaFLOPS of NVFP4 compute, with a 10× reduction in inference costs compared to Blackwell.

---

**🔴 The Hard Limits — where scaling is hitting walls**

**1. Transistor Density (Moore's Law slowing)**
Transistor density scaling has slowed materially below 5nm and approaches hard physical limits on gate length, leakage, and interconnect resistance. Energy-per-operation improvements are decelerating — typically 1.3–1.5× per node below 5nm, compared to 1.7–2× per node at older nodes. The doubling cadence of classical Moore's Law is no longer observed.

As technology nodes push toward 1nm and below, the size of transistors is approaching the physical scale of silicon atoms — traditional Moore's Law scaling is decelerating and becoming physically impossible.

**2. Power / Thermal Wall**
Power constraints will become the primary limiter on AI scaling. Despite efficiency improvements, the exponential growth in model size and inference demand means total power consumption will continue to rise. Data center operators will increasingly be limited by grid capacity rather than hardware availability. The Vera Rubin rack already draws 190–230 kW, up from ~130 kW for Blackwell — and requires all-liquid cooling.

**3. Memory (HBM) Supply Wall**
HBM is sold out for 2026, with new capacity not meaningfully impacting availability until 2027 and tightness forecast through 2028. Three suppliers — Samsung, SK Hynix, and Micron — control roughly 95% of global DRAM production, and they are rationally reallocating wafer capacity toward ultra-profitable HBM.

**4. Packaging (CoWoS) Bottleneck**
By mid-2026, CoWoS packaging utilization — not raw wafer starts — has become the binding constraint on AI hardware supply, with both CoWoS-S and CoWoS-L fully booked and lead times of 52–78 weeks. This directly killed the most ambitious version of Rubin Ultra: the original four-die version of the Rubin Ultra GPU — unveiled at GTC 2026 — has been cancelled due to manufacturing constraints TSMC cannot yet solve. The GPU that will actually ship in 2027 will deliver roughly half the compute and half the memory bandwidth of what was announced.

**5. Interconnect / Bandwidth Wall**
For single-rack deployments, Nvidia is pushing copper to its absolute physical limits. The Rubin Ultra NVL144 connects 144 GPUs using an all-copper scale-up network — beyond that, the industry is moving to co-packaged optics (CPO) to sustain bandwidth growth.

---

**🔵 How Nvidia is working around the walls**

Rather than just shrinking transistors, the strategy has shifted:

- **Chiplets** — gluing multiple dies together (B200 already uses 2 dies; 4-die designs planned)
- **Lower precision** — FP8 → FP4 → future FP2? Each halving doubles effective throughput
- **Rack-scale thinking** — the GB200 NVL72 and VR200 NVL72 treat an entire rack as "one GPU"
- **Sparsity** — exploiting zero-heavy matrices for 2× free speedup
- **Co-packaged Optics** — replacing copper with light for inter-GPU communication

---

**The bottom line:** Every technology hits a wall. The question isn't whether the wall exists — the mathematics proves it does. Constraints don't end progress. They redirect it. GPU performance will keep growing, but increasingly through clever packaging, rack-scale integration, and new precision formats — not from raw transistor shrinks alone.

---

**References:**

- [Nvidia GPU Roadmap 2026–2030 — VRLA Tech](https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/)
- [Rubin Ultra Four-Die GPU Cancelled — TechTimes](https://www.techtimes.com/articles/319410/20260701/nvidia-rubin-ultra-four-die-gpu-cancelled-packaging-limits-cut-2027-performance-half.htm)
- [HBM4 and Fab Limits — NextBigFuture](https://www.nextbigfuture.com/2026/07/hbm4-and-fab-limits-prevent-1000-vera-rubin-racks-per-day-in-2026-or-2027.html)
- [Hitting the Wall: Physical Limits of AI Chips — TetraMem](https://tetramem.com/hitting-the-wall-the-1d-2d-and-3d-physical-limits-threatening-the-future-of-ai-chips/)
- [The Memory Wall — SemiAnalysis](https://newsletter.semianalysis.com/p/the-memory-wall)
