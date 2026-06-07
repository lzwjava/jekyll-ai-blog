---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bottlenecks Shift, Blackwell Scales
translated: false
type: note
---

The production of NVIDIA’s Blackwell architecture (B200, GB200) over the past year has been a masterclass in industrial scaling—and a lesson in how bottlenecks simply shift rather than disappear.

While the Hopper generation (H100) defined 2023–2024, the last 12 months (mid-2025 to mid-2026) were defined by the massive, complex transition to Blackwell. Here is how TSMC and the supply chain handled that shift.

### 1. From Monoliths to Superchips (The Complexity Gap)

The biggest challenge TSMC faced this past year wasn't just volume; it was the **radical change in architecture**.

| Feature | Hopper (H100/H200) | Blackwell (B200/GB200) |
| --- | --- | --- |
| **Logic Design** | Monolithic (1 Die) | Multi-Die (2 GPU Dies + 1 CPU) |
| **HBM Memory** | 80–95 GB HBM3e | 192 GB HBM3e |
| **Packaging** | Standard CoWoS | CoWoS-L (Advanced 2.5D/3D) |
| **Interconnect** | NVLink | NVLink C2C (Chip-to-Chip) |

Producing a Blackwell GB200 "Superchip" means TSMC must fabricate two massive GPU dies and one Grace CPU, connect them with ultra-high-speed silicon bridges, and stack eight high-capacity HBM3e memory chips on top. This process is significantly more prone to failure than the previous generation.

### 2. The Bottleneck Evolution (2025–2026)

In the Hopper era, the bottleneck was **CoWoS capacity**. In the Blackwell era, the bottleneck became a **"Compound Constraint"**:

* **Advanced Packaging (CoWoS):** TSMC successfully scaled CoWoS capacity roughly tenfold since late 2023. By mid-2026, they reached an output of roughly **120,000 to 130,000 wafers per month** for advanced packaging. However, because Blackwell is so physically large and complex, it eats up "floor space" on the production line, effectively reducing the total number of chips that can be processed compared to smaller, simpler dies.
* **HBM3e Shortage:** Blackwell requires 192 GB of HBM3e per GPU. Global production of this specific memory (primarily from SK Hynix and Micron) has been fully allocated through the end of 2026. NVIDIA’s production volume is currently capped by how much HBM they can secure, not just how many silicon wafers TSMC can print.

### 3. Production Milestones of the Past Year

* **Late 2025 (The Ramp):** Blackwell achieved volume production. NVIDIA reported that Blackwell sales were "off the charts," with cloud providers fully absorbing every unit TSMC could deliver.
* **Early 2026 (U.S. Manufacturing):** A significant milestone occurred when the first NVIDIA Blackwell wafers were produced on U.S. soil at TSMC’s Arizona (Fab 21) facility. While not yet the primary source of volume, this marked the beginning of a supply chain diversification strategy.
* **Mid-2026 (The Shift to GB300):** As of June 2026, TSMC is already shifting focus. The "standard" Blackwell (B200) is becoming a mature product, and the industry is currently transitioning production capacity to the **Blackwell Ultra (GB300)** series, which offers even higher performance and memory density.

### Summary: By the Numbers

Industry analysts estimate that while Hopper production peaked in 2024, Blackwell has surpassed it in terms of total compute delivery. Despite the higher complexity:

* **Blackwell is now the dominant platform**, accounting for over **70% of NVIDIA’s high-end shipments** in 2026.
* **Wafer costs have surged.** With 3nm fabrication costs rising and the sheer size of the Blackwell dies, the cost per wafer has increased significantly, contributing to the premium pricing NVIDIA charges for the B200/GB200 systems.

TSMC’s ability to move Blackwell from a complex engineering design to a mass-produced "rack-scale" system in just one year is considered one of the most successful large-scale technology deployments in history, even if supply remains "constrained" to the point of being sold out through 2027.
