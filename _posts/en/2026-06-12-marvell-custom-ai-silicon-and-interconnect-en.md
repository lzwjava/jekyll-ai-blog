---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Marvell: Custom AI Silicon and Interconnect"
translated: false
type: note
---

**Question:** Give me an intro to Marvell, the chip company.

**Answer:**

Marvell Technology (NASDAQ: MRVL) is one of the most important semiconductor companies in the AI infrastructure buildout right now — arguably the #2 player behind Broadcom in custom AI silicon. Founded in 1995 by Sehat Sutardja, his wife Weili Dai, and his brother Pantas Sutardja, headquartered in Santa Clara, the company has ~7,480 employees and posted $8.19B revenue for fiscal 2026. Its first product was a CMOS-based read channel for disk drives — for its first two decades, Marvell was mostly known as a storage controller and networking chip vendor (your old hard drive likely had a Marvell controller in it).

**The pivot to data infrastructure.** The transformation began when Matt Murphy became CEO in 2016 and refocused the company on data center infrastructure and custom silicon. The $10B Inphi acquisition in 2021 brought critical electro-optics and interconnect technology, and revenue grew from $5.5B in fiscal 2023 to $8.2B in fiscal 2026. They also shed non-core businesses — in August 2025 they sold the automotive ethernet business to Infineon for $2.5B in cash.

**What they actually build today.** Three pillars matter for you as an AI engineer:

1. **Custom AI ASICs (XPUs)** — Marvell is the design partner when hyperscalers want their own accelerators instead of buying Nvidia GPUs. They've been associated with Amazon's Trainium and Google's Axion-adjacent work. The business model: the hyperscaler owns the architecture, Marvell supplies the physical design, advanced packaging, SerDes, HBM integration, and TSMC relationship. The custom AI chip TAM is projected to exceed $40B by 2028 as Amazon, Google, Microsoft, and Meta all scale proprietary silicon programs.

2. **Interconnect / electro-optics** — this is the Inphi DNA. PAM4 and coherent DSPs, laser drivers, trans-impedance amplifiers, silicon photonics, co-packaged optics, and linear pluggable optics chipsets. When you train across a 100k-GPU cluster, the optical links between racks run on this class of silicon. This is the part Jensen Huang cares about.

3. **Networking** — ethernet controllers, network adapters, PHYs, switches, and fibre channel adapters, plus DPUs (OCTEON line).

**Why it's hot right now.** At Computex 2026, Jensen Huang called Marvell the "next trillion-dollar company," and the stock soared almost 33% the next day — its biggest one-day gain ever. Nvidia had already committed a $2B investment in Marvell in March. Huang's reasoning maps directly to scaling-law economics: as computing spreads across enormous clusters, connectivity is what ties it all together — interconnect bandwidth, not FLOPs, is increasingly the bottleneck in frontier training runs. Marvell joins the S&P 500 on June 22, and the stock has returned 274% over the last 12 months. Guidance: ~$11.5B revenue in fiscal 2027 (+40% YoY), with the interconnect business growing more than 70%, and ~$16.5B projected for fiscal 2028.

**The mental model:** Nvidia sells the compute; Broadcom and Marvell sell the *alternative* compute (custom ASICs) plus the wiring that makes any of it work at cluster scale. Market cap sits around $220–253B, so the market is pricing it as a core AI infrastructure play, not a legacy chip vendor.

The main risk, straight from their own 10-K: heavy customer concentration in the data center end market, and the risk that customers vertically integrate and develop their own solutions — i.e., a hyperscaler building its own physical-design team is an existential threat to the ASIC business.

If you want to go deeper, the technically interesting threads are 224G SerDes design, PAM4 vs coherent DSP modulation, and co-packaged optics — these are where Marvell's moat actually lives.

**References:**

- [Marvell Q4 & FY2026 results (investor.marvell.com)](https://investor.marvell.com/news-events/press-releases/detail/1011/marvell-technology-inc-reports-fourth-quarter-and-fiscal-year-2026-financial-results)
- [Marvell FY2026 annual report (SEC)](https://www.sec.gov/Archives/edgar/data/0001835632/000110465926060265/tm261486d6_ars.pdf)
- [Marvell Technology — Wikipedia](https://en.wikipedia.org/wiki/Marvell_Technology)
- [MRVL — Yahoo Finance](https://finance.yahoo.com/quote/MRVL/)
- [Barchart: Marvell joins S&P 500 June 22](https://www.barchart.com/story/news/2407602/dear-marvell-technology-stock-fans-mark-your-calendars-for-june-22)
