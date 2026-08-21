---
audio: false
generated: true
image: false
lang: en
layout: post
title: Differences Between RTX 4090D and 4090
translated: false
type: note
---

**Question:** What are the differences between the RTX 4090D and RTX 4090?

**Answer:**

The RTX 4090D is a China-exclusive variant of the RTX 4090, created specifically to comply with US export restrictions. Here's a breakdown:

**Why it exists**

US export controls banned shipments of the full-spec RTX 4090 to China due to its AI compute capability exceeding regulatory thresholds. NVIDIA launched the RTX 4090D ("D" for "Domestic") exclusively for the mainland Chinese market.

**Key spec differences**

| | RTX 4090 | RTX 4090D |
|---|---|---|
| CUDA Cores | 16,384 | 14,592 |
| TDP | 450W | 425W |
| Memory | 24GB GDDR6X | 24GB GDDR6X |

The 4090D uses the AD102-250 GPU with fewer cores, but is otherwise largely identical to the standard 4090.

**Performance gap**

The 4090D generally performs around 95% of the RTX 4090 — roughly a 5% difference in most scenarios. In gaming benchmarks at 2K or 4K, frame rate differences are typically in the single digits.

**Overclocking caveat**

ASUS's custom ROG Strix RTX 4090D can push TDP from 425W up to 600W via overclocking, which has actually allowed it to *outperform* the standard RTX 4090 in some benchmarks.

In short: the 4090D is a slightly nerfed version for the Chinese market, with ~5–10% lower performance depending on workload, but the same VRAM and a slightly lower power draw.

**References:**
- [RTX 4090 China Guide: 4090 vs 4090D Explained](https://electronics.alibaba.com/buyingguides/rtx-4090-china-guide-4090-vs-4090d-explained)
- [RTX 4090 vs 4090D – Oreate AI Blog](https://www.oreateai.com/blog/rtx-4090-vs-4090d-unpacking-the-nuances-of-nvidias-flagship-gpus/346eabc62c7e033966dab3fef1107ca4)
- [ASUS RTX 4090D Outperforming RTX 4090 – Game Rant](https://gamerant.com/asus-rtx-4090d-outperforming-rtx-4090/)
