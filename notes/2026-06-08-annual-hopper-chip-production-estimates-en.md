---
audio: false
generated: true
image: false
lang: en
layout: post
title: Annual Hopper Chip Production Estimates
translated: false
type: note
---

Question: How many H100, H200, or H800 chips do NVIDIA and TSMC produce in one year?

Answer:

Because NVIDIA designs the chips but relies entirely on TSMC (Taiwan Semiconductor Manufacturing Company) for fabrication and advanced advanced packaging (CoWoS), their combined annual production capacity has scaled dramatically over the last few years to meet unprecedented AI demand.

The production numbers are calculated in terms of **total volume across the Hopper family** (which includes the **H100**, the upgraded **H200**, and the China-specific export-compliant **H800** and **H20** variants), as they all share the same base silicon architecture and manufacturing pipelines.

---

## Annual Production Timeline (Estimates)

### 1. 2023 Production: ~500,000 to 1 Million Chips

* **The Bottle Neck:** Production in 2023 was highly bottlenecked by TSMC's limited **CoWoS (Chip-on-Wafer-on-Substrate)** packaging capacity, rather than raw wafer manufacturing.
* **Breakdown:** TSMC shipped roughly **500,000 to 550,000** flagship H100 units in the first half/mid-2023. By the end of the year, as secondary supply lines opened, cumulative production approached close to **1 million H100 equivalents**. This included initial runs of the H800 before tighter U.S. export controls were introduced in late 2023.

### 2. 2024 Production: ~3.5 Million to 5 Million Chips

* **The Ramp-Up:** This was the peak production period for the Hopper generation. TSMC drastically expanded its high-end packaging factories, and NVIDIA supplemented its supply chain by utilizing alternative advanced packaging foundries (such as Intel Foundry Services).
* **Breakdown:** Total production for 2024 reached an upper bound of roughly **4 to 5 million Hopper-generation GPUs**.
* The **H100** accounted for the bulk of early 2024 shipments.
* The **H200** (featuring faster HBM3e memory) entered mass production in mid-2024 and overtook the H100 as the primary flagship.
* The **H800** was mostly phased out due to updated sanctions and replaced by the heavily altered **H20** model for the Chinese market.



### 3. 2025 – 2026 Shift: Decline in Hopper Production

* **The Transition:** By 2025 and moving into 2026, production lines at TSMC heavily shifted away from the Hopper architecture to prioritize NVIDIA's next-generation **Blackwell architecture (B100, B200, GB200)** and subsequent **Blackwell Ultra / GB300** lines.
* **Current Status:** Combined H100 and H200 sales dropped sharply from hundreds of thousands per quarter in 2024 down to minimal maintenance levels by late 2025/2026, as cloud providers transitioned fully to Blackwell.

---

## The Technical Limit: How many chips per wafer?

The Hopper GPU (GH100 die) is physically massive, measuring roughly **814 mm²**.

* A standard 300mm silicon wafer can mathematically fit about **86** of these giant chips.
* Due to unavoidable manufacturing defects on such a large scale, the "yield rate" (the percentage of functional chips per wafer) is typically around **65% to 70%**.
* This means TSMC gets roughly **55 to 60 usable Hopper chips per wafer** before putting them through the complex CoWoS packaging process.

References:

* [When Do More AI Chips for China Mean Fewer for the United States? - IFP.org](https://ifp.org/ai-chip-supply-diversion/)
* [Estimates of GPU or equivalent resources of large AI players for 2024/5 - LessWrong](https://www.lesswrong.com/posts/bdQhzQsHjNrQp7cNS/estimates-of-gpu-or-equivalent-resources-of-large-ai-players)
* [Nvidia reportedly selects Intel Foundry Services for GPU packaging production - Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidia-reportedly-selects-intel-foundry-services-for-chip-packaging-production-could-produce-over-300000-h100-gpus-per-month)
* [The stock of computing power from NVIDIA chips is doubling every 10 months - Epoch AI](https://epoch.ai/data-insights/nvidia-chip-production)
