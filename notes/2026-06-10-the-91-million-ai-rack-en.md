---
audio: false
generated: true
image: false
lang: en
layout: post
title: The $9.1 Million AI Rack
translated: false
type: note
---

Question: Why will NVIDIA's Rubin AI rack (NVL72) be so expensive, with estimates reaching up to $9.1 million per cabinet?

Answer: Recent 2026 financial and supply chain reports from investment firms like Bernstein Research and Morgan Stanley have broken down the staggering cost of NVIDIA’s next-generation **Vera Rubin NVL72** server rack (referred to as a "柜" or cabinet). While Morgan Stanley initially estimated the cost at around $7.8 million, Bernstein’s updated data projects it could reach **$9.1 million per rack**.

The price is driving a massive spike compared to the previous Blackwell generation (which costs sub-$4 million) due to several severe hardware and supply chain constraints:

### 1. Massive Surges in Memory and Storage Costs (~$3.2 Million)

Memory is the single largest factor driving up the price, seeing a staggering **435% to 485% increase** in cost compared to older architectures.

* **HBM4 Price Explosion:** The Rubin architecture adopts next-generation **High Bandwidth Memory (HBM4)**. Due to intense AI demand and manufacturing complexities, HBM4 prices are projected to soar up to **$53 per gigabyte**. The HBM4 components alone account for roughly **$1.09 million** per rack.
* **System RAM & Storage:** The system relies heavily on expensive LPDDR5X memory (accounting for **$800,000**) and directly attached 3D NAND storage (accounting for **$1.28 million**). Volatile flash and DRAM market pricing in 2026 has significantly pushed these figures beyond initial expectations.

### 2. High Density of Premium Processors (~$4.14 Million)

* **72 Rubin GPUs:** A single NVL72 cabinet packs 72 next-generation Rubin GPUs. At an estimated volume price of **$55,000 per GPU**, the graphics processors alone make up nearly half the rack's cost at **$3.96 million**.
* **36 Vera CPUs:** The cabinet also includes 36 high-performance Vera CPUs, which add another **$180,000** ($5,000 per chip).

### 3. Sophisticated Networking and Infrastructure (~$1.27 Million)

To connect 72 GPUs and keep data flowing without bottlenecks, the architectural infrastructure has become exponentially more complex:

* **Advanced Switching:** Includes roughly **$250,000** for high-speed NVLink switches and **$200,000** for Spectrum-X networking switches.
* **Cabling & Backplanes:** Complex physical routing, copper/optical cabling, and backplanes add about **$620,000**.

### 4. Advanced Materials and Engineering Limits (~$500,000)

* **Ultra-Premium PCBs:** The printed circuit boards have been significantly upgraded. For instance, the switch tray PCB scales from 24 layers up to 32 layers, using much higher material grades (moving from M7 to M8 standards). This pushes overall PCB costs up by **233%** (reaching around $117,000).
* **Cooling and Power:** Drawing a massive **220 kW of power** per cabinet, the specialized liquid cooling systems (~$160,000) and heavy-duty power delivery systems (~$150,000) add to the heavy premium.

While a single cabinet costs nearly $9.1 million, cloud giants continue to buy them because the sheer compute efficiency and bandwidth per dollar still heavily outperform previous architectures for training and deploying frontier AI models.

References:

* [Bernstein Warns NVIDIA's Vera Rubin Racks Will Hit $9.1 Million as HBM4 Prices Triple to $53 Per Gigabyte](https://wccftech.com/bernstein-warns-nvidias-vera-rubin-racks-will-hit-9-1-million-as-hbm4-prices-triple-to-53-per-gigabyte/)
* [Nvidia's memory costs soar 485%, latest AI systems now cost $7.8 million to build — memory now comprises 25% of the total cost](https://www.google.com/search?q=https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidias-memory-costs-soar-485-percent-latest-ai-systems-now-cost-usd7-8-million-to-build-memory-now-comprises-25-percent-of-the-total-cost)
* [Nvidia's Vera Rubin Rack Price Soars to $7.8 Million; PCB, MLCC, Memory Costs Collectively Double](https://finance.biggo.com/news/MrEuTZ4BX0tZvRTv67Pr)
