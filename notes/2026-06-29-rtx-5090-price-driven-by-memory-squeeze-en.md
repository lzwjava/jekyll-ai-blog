---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 5090 Price Driven by Memory Squeeze
translated: false
type: note
---

Question: Is the RTX 5090 price surge driven by AI/compute demand — 32GB GDDR7 attractive for local LLM inference/training, export-restricted datacenter cards in China pushing prosumer demand, plus DRAM/GDDR cost pressure in 2025–2026?

Let me verify the specifics rather than just agreeing.Question: Is the RTX 5090 price surge driven by AI/compute demand — 32GB GDDR7 making it attractive for local LLM inference/training, export-restricted datacenter cards in China pushing prosumer demand, plus DRAM/GDDR cost pressure in 2025–2026?

Answer:

Mostly right on the macro forces, but your causal emphasis is slightly off. The dominant driver isn't direct demand for the 5090 as an AI card — it's an upstream **memory supply squeeze** where AI datacenter buildouts are starving the GDDR7 channel.

**What the evidence actually shows:**

The primary mechanism is wafer allocation, not consumer-side AI demand for 5090s. AI workloads could consume nearly 20% of global DRAM wafer capacity in 2026 when factoring in both HBM and GDDR7 demand. HBM alone consumes roughly three times the wafer capacity of DDR5 per gigabyte, while GDDR7 requires approximately 1.7 times the wafer area of standard consumer DRAM. Because foundries earn significantly higher margins on HBM, they have deprioritized GDDR7 allocations — creating the supply deficit.

The BOM concentration is what makes the 5090 uniquely exposed. Because the RTX 5090 carries a 32GB GDDR7 footprint across a 512-bit memory bus, its production costs are acutely sensitive to memory price swings. Memory accounts for over 80% of the total bill of materials for the RTX 5090. So the same 32GB that makes it attractive for local inference is *also* its cost vulnerability — but the price movement is driven by the input cost, not by inference buyers bidding it up.

Nvidia is actively reallocating fab/memory away from gaming. Nvidia is reportedly cutting gaming GPU production by 30-40% to prioritize higher-margin data center chips like the H100 and H200. And specifically: when manufacturers allocate scarce memory chips, they prioritize high-margin AI accelerators over gaming cards.

The wholesale pass-through is concrete: Nvidia implemented a $300 USD wholesale price adjustment for its flagship GeForce RTX 5090 and the China-market variant RTX 5090D V2, effective May 13, 2026. Note the MSRP fiction — the actual sales price is twice as high as the original MSRP, which is still listed at $1,999 on NVIDIA's website.

**Where your framing needs correction:**

1. **"AI/compute demand surge" as the driver** — too direct. The surge is for *datacenter HBM*, which crowds out GDDR7 at the foundry level. The 5090 is collateral damage, not the target. This distinction matters because it means waiting for "AI hype to cool" won't help — it's structural. Relief won't arrive until 2028 when Micron's new HBM manufacturing comes online.

2. **China export-restriction angle** — plausible but **not supported in these sources** as a named price driver. The documents mention the RTX 5090D V2 as the China-market variant but attribute the price action to GDDR7 costs, not to H100/H200 export bans pushing Chinese buyers into prosumer cards. That's a reasonable hypothesis (and the 5090D exists precisely because of export tiering), but treat it as your inference, not established fact. The actual restriction substitution in China historically channels toward smuggled datacenter cards and domestic accelerators (Huawei Ascend), not consumer 5090s at scale.

3. **"Memory price increases compounded the squeeze"** — correct, and stronger than you stated. Memory prices have risen by several hundred per cent in recent months. DRAM prices are forecast to rise 40% by Q2 2026. This isn't a compounding side-factor; it *is* the squeeze.

**Net:** Your three forces are real, but reorder them: (1) AI/HBM crowding out GDDR7 at the foundry → (2) GDDR7 scarcity + ~80% memory BOM → (3) Nvidia cutting gaming production and passing costs through. The China/export angle is a defensible secondary hypothesis the sources don't confirm.

References:

- [Why RTX 5090 Prices Keep Climbing — BuySellRam](https://www.buysellram.com/blog/why-rtx-5090-prices-keep-climbing-nvidias-wholesale-hike-and-the-gddr7-shortage-behind-it/)
- [RTX 5090 Prices Hit $4K: Memory Crisis Why — byteiota](https://byteiota.com/rtx-5090-prices-hit-4k-5k-coming-memory-crisis-why/)
- [GPU pricing set for reset as AI-driven memory shortages push costs higher — Astute Group](https://www.astutegroup.com/news/general/gpu-pricing-set-for-reset-as-ai-driven-memory-shortages-push-costs-sharply-higher/)
- [NVIDIA Slashes RTX 50 Series Production Amid Memory Shortage — Roic News](https://www.roic.ai/news/nvidia-slashes-rtx-50-series-gpu-production-amid-memory-shortage-and-ai-demand-shift-02-05-2026)
- [NVIDIA Prepares RTX 5090 Price Hike Amid Rising GDDR7 Costs — TechPowerUp](https://www.techpowerup.com/349050/nvidia-reportedly-prepares-rtx-5090-price-hike-amid-rising-gddr7-costs)
