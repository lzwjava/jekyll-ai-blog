---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huawei's Tao Law Chip Breakthrough
translated: false
type: note
---

Question: What is Huawei's "Tao Law" and how is Huawei making breakthroughs with chips?

Answer:

### What is Huawei's "Tao Law" ($\tau$ Scaling Law)?

The **Tao Law** (officially presented as the **Tau ($\tau$) Scaling Law**) is a new semiconductor development framework unveiled by Huawei at the IEEE ISCAS conference. It is designed to serve as an alternative roadmap to Moore's Law, which has traditionally guided the chip industry by relying on "geometric scaling"—physically shrinking transistors to boost performance.

Because US sanctions have restricted China's access to advanced lithography equipment (like ASML's EUV machines) required for extreme geometric shrinking, Huawei's Tao Law shifts the focus from physical size to **"time ($\tau$) scaling."**

* **The Principle:** Instead of focusing strictly on making transistors smaller, the Tao Law prioritizes system-level optimization by continuously compressing signal propagation delay ($\tau$, the time constant) and utilizing technologies like **"LogicFolding."**
* **The Goal:** By redesigning how information flows through a chip and utilizing advanced 3D-IC packaging, chiplets, and multi-die vertical stacking, Huawei aims to achieve the equivalent performance and transistor density of a **1.4 nm (14 Ångström) process by 2031**, even while using less advanced lithography equipment.

---

### How Huawei is Making Breakthroughs with Chips

Huawei’s strategy to bypass Western semiconductor blockades relies on architecture, software, and domestic supply chain integration:

* **Advanced Packaging & Heterogeneous Integration (Chiplets):** Since Huawei cannot easily manufacture monolithic 3nm or 2nm dies, they stack multiple mature-node dies vertically and horizontally. This 3D-IC architecture binds logic chips with High Bandwidth Memory (HBM) using sophisticated domestic packaging techniques to mimic the performance of a single, highly advanced processor.
* **Architectural Innovation (LogicFolding):** Rather than traditional linear chip layouts, Huawei utilizes architectural folding mechanisms to dramatically shorten the physical distance signals must travel inside the silicon, reducing latency and power consumption.
* **Accelerating AI Chips (The Ascend Series):** Huawei has aggressively scaled its domestic AI hardware to challenge Nvidia within mainland China. Their **Ascend 950PR** processor entered mass production, capturing a majority of domestic AI infrastructure orders, with an upgraded **Ascend 950DT** following closely behind.
* **Unified Domestic Ecosystem:** Huawei has successfully decoupled its hardware from Western software dependencies. By pairing their Kunpeng (CPU) and Ascend (AI) hardware with MindSpore (AI framework) and EulerOS/HarmonyOS, they maximize hardware efficiency through optimized software, proving that systemic coordination can offset limitations in raw fabrication precision.

References:

* [HUAWEI Presents the Tau (τ) Scaling Law](https://www.huawei.com/en/news/2026/5/ieee-iscas-tau-scaling)
* [Huawei's “Tao Law” Sparks a New Advanced Packaging Race](https://www.istart-tek.com/en/2026/06/01/11421/)
* [华为推出“韬定律” 改写全球半导体规则](https://www.news.cn/tech/20260526/75603364bbae42bab67933d63d63e373/c.html)
