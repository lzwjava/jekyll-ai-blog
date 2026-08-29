---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4090 Die and VRAM Costs
translated: false
type: note
---

**Question:** How much do the GPU die and VRAM cost to manufacture in the NVIDIA RTX 4090?

**Answer:**

NVIDIA doesn't publicly disclose its Bill of Materials (BOM), but industry analysts have pieced together credible estimates. Here's a breakdown:

---

### 🔲 GPU Die (AD102)

The AD102 die is built on TSMC's 4nm EUV (4N) process, packs 76.3 billion transistors, and measures 608 mm².

With that die size, NVIDIA can only get around **~90 full dies per wafer**. TSMC's 4N node reportedly costs at least twice as much as older nodes — meaning the AD102 costs more than twice per chip compared to the previous-gen GA102 (RTX 3090).

Independent analysts estimate the AD102 GPU die costs roughly **$175–$200 USD（约 ¥1,270–¥1,450 CNY）** to manufacture.

---

### 🧠 VRAM (24 GB GDDR6X)

The RTX 4090 carries 24 GB of GDDR6X on a 384-bit interface at 21 Gbps (~1 TB/s bandwidth). GDDR6X is among the most expensive consumer memory, estimated at roughly **$8–$10 per GB（约 ¥58–¥73/GB）** at volume pricing — putting the full 24 GB stack at approximately **$190–$240 USD（约 ¥1,380–¥1,740 CNY）**.

---

### 💰 Full BOM Estimate

| Component | USD | CNY |
|---|---|---|
| AD102 GPU Die | ~$175–$200 | ~¥1,270–¥1,450 |
| 24 GB GDDR6X VRAM | ~$190–$240 | ~¥1,380–¥1,740 |
| PCB, VRMs, cooling, connectors | ~$80–$150 | ~¥580–¥1,090 |
| **Total BOM (est.)** | **~$450–$600** | **~¥3,270–¥4,350** |

---

### 📊 Cost vs. Retail Price

The card launched at **$1,599 MSRP（约 ¥11,600 CNY）** in October 2022. As of mid-2026, street prices run **$2,400–$2,800（约 ¥17,400–¥20,300 CNY）**, well above launch price because NVIDIA ended production in late 2024 and AI demand for 24 GB VRAM remains high.

The ~$450–$600 manufacturing cost vs. a $1,600–$2,800 retail price reflects NVIDIA's estimated **60%+ gross margin** on flagship consumer GPUs — the gap between raw silicon and what you pay at retail is enormous.

---

**References:**
- [Why Nvidia's RTX 4080, 4090 Cost so Damn Much — Tom's Hardware](https://www.tomshardware.com/news/why-nvidias-4080-4090-cost-so-damn-much)
- [Spitballing Nvidia's RTX 5090 GPU Die Manufacturing Costs — Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/spitballing-nvidias-gb202-gpu-die-manufacturing-costs-die-could-cost-as-little-as-usd290-to-make)
- [RTX 4090 Doesn't Max-Out AD102 — TechPowerUp](https://www.techpowerup.com/299091/nvidia-rtx-4090-doesnt-max-out-ad102-ample-room-left-for-future-rtx-4090-ti)
- [NVIDIA RTX 4090: Specs, 24GB VRAM, Price & AI Performance — RunPod](https://www.runpod.io/articles/guides/nvidia-rtx-4090)
