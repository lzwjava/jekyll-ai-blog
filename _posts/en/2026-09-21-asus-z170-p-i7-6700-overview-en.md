---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS Z170-P i7-6700 Overview
translated: false
type: note
---

Question: **Intro to the ASUS Z170-P + Intel Core i7-6700 combo**

Answer: This is a **2015-era Intel Skylake desktop platform**: ASUS Z170-P motherboard + Intel Core i7-6700, with the original Intel stock cooler. It was a fairly solid mainstream/high-end setup for its generation.

### Hardware overview

| Part                | Specs                                                         |
| ------------------- | ------------------------------------------------------------- |
| **CPU**             | Intel Core i7-6700                                            |
| **Architecture**    | Skylake, 14 nm                                                |
| **Cores / Threads** | 4C / 8T                                                       |
| **Base / Turbo**    | 3.4 / 4.0 GHz                                                 |
| **Cache**           | 8 MB                                                          |
| **TDP**             | 65 W                                                          |
| **Socket**          | LGA1151                                                       |
| **iGPU**            | Intel HD Graphics 530                                         |
| **Motherboard**     | ASUS Z170-P                                                   |
| **Memory**          | DDR4                                                          |
| **Storage**         | 4× SATA 6 Gb/s + 1× M.2                                       |
| **Expansion**       | PCIe 3.0, including x16 GPU slot                              |
| **Rear I/O**        | USB 3.0, USB-C, USB 2.0, HDMI, DVI-D, Gigabit Ethernet, audio |

Intel lists the i7-6700 at **4 cores / 8 threads, 3.4 GHz base and up to 4.0 GHz turbo**, with 65 W TDP and HD Graphics 530. ([Intel][1])

The Z170-P uses **LGA1151** and supports 6th-gen Core processors. It has four DDR4 DIMM slots, an M.2 slot supporting 2242/2260/2280 devices, and four SATA 6 Gb/s ports. ([ASUS Download Center][2])

### What this means today

The interesting part is that **the CPU is still perfectly usable for basic desktop/server work**, but the platform is old:

```text
i7-6700
  ├── 4 physical cores
  ├── 8 threads
  ├── 3.4 GHz base
  └── 4.0 GHz turbo
        │
        ▼
    ASUS Z170-P
        │
   ┌────┴─────┐
   ▼          ▼
 DDR4       PCIe 3.0
   │          │
 RAM       GPU / NIC
        │
        ▼
     M.2 / SATA
```

For a **cheap second-hand machine**, this combo can still make sense for:

* Linux homelab / small server
* NAS
* Router/firewall
* Lightweight Docker workloads
* Older games
* General desktop use
* Development machine
* GPU-powered workloads where the CPU isn't the bottleneck

For modern CPU-heavy workloads, however, **4C/8T is the main limitation**. Also, the i7-6700 is officially end-of-servicing, with Intel listing September 30, 2022 as its end-of-servicing-updates date. ([Intel][1])

One useful detail: **the i7-6700 is not the 6700K**. The 6700 has a locked multiplier, so you shouldn't buy this expecting a typical Z170 overclocking setup.

If you're looking at this **second-hand listing**, send me the **asking price** and I can tell you whether the combo makes sense in 2026, including what RAM/GPU/SSD you should pair with it.

References:

* [Intel Core i7-6700 specifications](https://www.intel.com/content/www/us/en/products/sku/88196/intel-core-i76700-processor-8m-cache-up-to-4-00-ghz/specifications.html?utm_source=chatgpt.com)
* [ASUS Z170-P manual/specifications](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-P/E12045_Z170-P_UM_V3_WEB.pdf?utm_source=chatgpt.com)

[1]: https://www.intel.com/content/www/us/en/products/sku/88196/intel-core-i76700-processor-8m-cache-up-to-4-00-ghz/specifications.html?utm_source=chatgpt.com "Intel® Core™ i7-6700 Processor"
[2]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-P/E12045_Z170-P_UM_V3_WEB.pdf?utm_source=chatgpt.com "Z170-P specifications summary"
