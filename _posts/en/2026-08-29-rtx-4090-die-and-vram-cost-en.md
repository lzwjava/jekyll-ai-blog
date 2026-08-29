---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4090 Die and VRAM Cost
translated: false
type: note
---

**Question:** How much do the GPU die and VRAM cost to manufacture in the NVIDIA RTX 4090?

**Answer:**

NVIDIA doesn't publicly disclose its Bill of Materials (BOM), but industry analysts have pieced together credible estimates. Here's a breakdown:

---

### 🔲 GPU Die (AD102)

The AD102 die is built on TSMC's 4nm EUV (4N) process, packs 76.3 billion transistors, and measures 608 mm².

With that die size, NVIDIA can only get around **~90 full dies per wafer**. TSMC's 4N node reportedly costs **at least twice as much** as older nodes like TSMC N7/N6 — meaning the AD102 costs more than twice per chip compared to the previous-gen GA102 used in the RTX 3090.

Independent analysts estimate the AD102 GPU die costs roughly **$175–$200** to manufacture, though this figure has likely changed since it was calculated.

---

### 🧠 VRAM (24 GB GDDR6X)

The RTX 4090 carries **24 GB of GDDR6X** memory on a 384-bit interface running at 21 Gbps, delivering roughly 1 TB/s of memory bandwidth.

NVIDIA does not disclose memory contract pricing, but GDDR6X is among the most expensive consumer memory available. Industry estimates place GDDR6X at roughly **$8–$10 per GB** at volume pricing, putting the 24 GB stack at approximately **$190–$240** in raw VRAM cost — making the memory subsystem comparable in cost to the die itself.

---

### 💰 Full Picture (Estimated BOM)

| Component | Estimated Cost |
| --- | --- |
| AD102 GPU Die | ~$175–$200 |
| 24 GB GDDR6X VRAM | ~$190–$240 |
| PCB, VRMs, cooling, connectors | ~$80–$150 |
| **Total BOM (est.)** | **~$450–$600** |

On top of raw materials, NVIDIA also factors in R&D, engineering, TSMC wafer reservation costs, and packaging — and then NVIDIA, AIB partners, and retailers all stack their own margins before the card reaches consumers.

The card launched at **$1,599 MSRP** in October 2022, and as of mid-2026, street prices typically run **$2,400–$2,800**, well above launch price because NVIDIA ended production in late 2024 and AI demand for 24 GB VRAM remains high.

So the ~$450–$600 in manufacturing cost vs. a $1,600–$2,800 retail price reflects NVIDIA's notoriously high margins — estimated at roughly **60%+ gross margin** on flagship consumer GPUs.

---

**References:**

- [Why Nvidia's RTX 4080, 4090 Cost so Damn Much — Tom's Hardware](https://www.tomshardware.com/news/why-nvidias-4080-4090-cost-so-damn-much)
- [Spitballing Nvidia's RTX 5090 GPU Die Manufacturing Costs — Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/spitballing-nvidias-gb202-gpu-die-manufacturing-costs-die-could-cost-as-little-as-usd290-to-make)
- [RTX 4090 Doesn't Max-Out AD102 — TechPowerUp](https://www.techpowerup.com/299091/nvidia-rtx-4090-doesnt-max-out-ad102-ample-room-left-for-future-rtx-4090-ti)
- [NVIDIA RTX 4090: Specs, 24GB VRAM, Price & AI Performance — RunPod](https://www.runpod.io/articles/guides/nvidia-rtx-4090)
- [How Much Is the RTX 4090's Production Cost? — Quora](https://www.quora.com/How-much-is-the-RTX-4090-s-production-cost-Is-it-overpriced-If-it-is-how-much-do-you-think-it-should-cost)
