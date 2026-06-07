---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA Rubin vs Blackwell Architecture
translated: false
type: note
---

Question: How does the upcoming NVIDIA Rubin AI platform differ from Blackwell in terms of architecture and production requirements?

Answer:

NVIDIA's architecture roadmap has shifted from the Blackwell platform (the current enterprise workhorse) to the newly ramping **Vera Rubin** platform (slated for late 2026 hyperscaler deployments). While Blackwell focused on raw scaling via dual-die stitching, Rubin represents a fundamental leap designed specifically for **Agentic AI**—deep reasoning workloads that execute complex multi-step tasks.

The differences between Blackwell and Rubin span both physical architecture and the immense pressure they place on TSMC's manufacturing ecosystem.

---

## 1. Architectural Differences

The transition from Blackwell to Rubin changes the math on AI compute by shattering the "memory wall" and shifting processor layouts.

| Feature | Blackwell (B200 / B300) | Rubin (R100) | The Architectural Leap |
| --- | --- | --- | --- |
| **Compute Performance** | 9 to 10 PFLOPS (FP4) | **50 PFLOPS (FP4)** | A 5x throughput increase using a 3rd-Gen Transformer Engine. |
| **Memory Technology** | HBM3e | **HBM4** | Moves to a native 12-Hi vertical stacking standard. |
| **Memory Bandwidth** | 8 TB/s | **22 TB/s** | Nearly a **3x increase** in bandwidth to feed data into processing cores without latency. |
| **Interconnect** | NVLink 5 (1.8 TB/s) | **NVLink 6 (3.6 TB/s)** | Doubles the inter-GPU communication bandwidth, critical for massive Mixture-of-Experts (MoE) models. |
| **Companion CPU** | Grace CPU (ARM-based) | **Vera CPU** | Packs 88 custom Olympus ARM cores with 1.5 TB of on-chip LPDDR5X memory. |

### The Chiplet Shift

Blackwell relies on a flat, monolithic-style stitching of two identical dies over a high-speed interconnect. Rubin introduces a **multi-process node chiplet design**.

* The core compute logic is built on cutting-edge **TSMC 3nm** architecture.
* The less intensive Input/Output (I/O) logic is separated onto more cost-effective **5nm** chiplets.
* This mixed-node strategy maximizes compute density where it matters most while controlling overall manufacturing costs.

---

## 2. Production & Semiconductor Requirements

Building Rubin requires a completely different manufacturing playbook from TSMC, forcing a rapid evolution in advanced packaging.

### From 2.5D CoWoS to 3D Vertical Stacking (SoIC)

Blackwell is built on TSMC's 4NP node and relies on 2.5D **CoWoS-L** packaging (placing the dies flat side-by-side on a substrate alongside memory).

Because Rubin is incredibly dense, a flat layout would make the chip so physically massive that it would warp or break during manufacturing. To bypass this "reticle wall," TSMC is using **SoIC (System on Integrated Chips)** technology for Rubin. This allows 3D vertical stacking—stacking parts of the compute logic directly on top of each other before attaching the external HBM4 memory stacks via CoWoS.

### The HBM4 Yield Challenge

Blackwell utilizes mature HBM3e memory. Rubin is the first platform to adopt **HBM4**, which utilizes a custom logic base die that must be fabricated directly by TSMC rather than memory vendors (like SK Hynix or Micron). Due to the complexity of integrating 12-Hi memory layers, yield issues originally forced NVIDIA to scale back its upcoming "Rubin Ultra" variant from a rumored 4-die layout to a safer 2-die layout to ensure mass-production viability.

### Crucial Crowding of the 3nm Node

While Blackwell safely consumed TSMC's highly optimized 4nm capacity, Rubin relies heavily on the **TSMC 3nm (N3P) node**. Market data indicates that AI applications will claim roughly 36% of all TSMC 3nm capacity, creating a major supply-chain bottleneck as NVIDIA competes for allocation against hyperscalers building custom silicon (like Google's TPU v7/v8 and Amazon's Trainium v3).

---

## 3. Data Center Infrastructure Requirements

The differences extend beyond the silicon and into the physical real estate of the data center.

* **The Power Wall:** A standard Blackwell rack (NVL72) draws up to 120kW of power. The corresponding **Vera Rubin NVL72** rack is projected to double that power density.
* **45°C Hot Water Cooling:** Because fans can no longer cool a system this dense, Rubin introduces single-phase Direct Liquid Cooling (DLC) that functions with water as warm as **45°C (113°F)**. This eliminates the need for massive mechanical chillers entirely, making Rubin completely fanless and tubeless inside the rack—but it means Rubin *cannot* be deployed in traditional, air-cooled data centers.

References:

* [NVIDIA Rubin Architecture Deep Dive: The $500B AI Supercycle - ServerMO](https://www.servermo.com/blogs/nvidia-rubin-gpu-architecture-guide/)
* [NVIDIA Rubin GPU: Advancements in Process and Packaging Technologies - Semicon](https://www.semicone.com/article-179.html)
* [NVIDIA's Rubin Ultra Seen Sticking to Dual-Die Design on Packaging Constraints - TrendForce](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/)
* [NVIDIA Vera Rubin Ramps Into Full Production to Power Agentic AI Factories Worldwide - NVIDIA News](https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory)
