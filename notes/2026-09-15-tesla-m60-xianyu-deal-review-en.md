---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M60 Xianyu Deal Review
translated: false
type: note
---

**Question:** Is the Tesla M60 16GB being sold on Xianyu (described as pulled from server, cosmetic wear, functional, no repairs, plug-and-play) a good buy? The listing claims it suits AI, rendering, modeling, virtualization — and notes the fan shroud was removed.

**Answer:**

Let me be upfront: the M60 is a **very different card from the P100**, and several of the seller's claims are misleading or simply wrong. Here's a full breakdown:

---

**What the Tesla M60 Actually Is**

The M60 is a **Maxwell-architecture** (2015) GPU designed primarily for **NVIDIA GRID virtual desktop infrastructure (VDI)** — think remote workstations for enterprises, not compute or AI acceleration. It has:

- **2× GM204 dies** on a single board = 2× 8GB = 16GB total, but the two dies are **not unified memory** — each 8GB pool is independent
- **FP32:** ~9.6 TFLOPS combined (both dies)
- **No FP16 acceleration** (Maxwell has no native FP16 compute — it falls back to FP32 speed)
- **No Tensor Cores** (that came with Volta in 2017)
- **TDP: 300W** — actually *higher* than the P100
- PCIe x16, passive cooling (needs server airflow or direct fan, same situation as P100)

---

**Evaluating the Seller's Claims**

| Claim | Reality |
| --- | --- |
| "适合AI" (Good for AI) | ❌ Weak — no FP16, no Tensor Cores, poor CUDA compute efficiency |
| "渲染/建模" (Rendering/Modeling) | ⚠️ Partial — Maxwell supports OpenGL/DirectX but it's a decade-old arch |
| "虚拟化" (Virtualization/VDI) | ✅ This is literally what it was designed for — GRID vGPU |
| "专业图形加速, CAD/PS/3D" | ❌ Misleading — it has no display outputs; requires Quadro/workstation drivers for CAD professional features |
| "低功耗静音" (Low power, quiet) | ❌ False — 300W TDP, passive cooler, loud fan required |
| "即插即用多屏输出" (Plug & play multi-display) | ❌ Wrong — the M60 has **no video outputs at all**; it's a headless server card |
| "风扇外壳拆掉" (Fan shroud removed) | ⚠️ You need to DIY a cooling solution, same as P100 |

---

**M60 vs P100 — Which is Better?**

| | Tesla M60 | Tesla P100 |
| --- | --- | --- |
| Architecture | Maxwell (2015) | Pascal (2016) |
| VRAM | 2× 8GB (split) | 16GB unified HBM2 |
| FP16 | ❌ No | ✅ Yes |
| Tensor Cores | ❌ No | ❌ No (Pascal gen) |
| Memory Bandwidth | 320 GB/s | **732 GB/s** |
| Best Use | VDI / GRID | Compute / AI / HPC |
| Market Price | ~$30–60 USD | ~$76–150 USD |

The P100 wins in almost every compute dimension. The M60's split memory architecture is also a real limitation — you can't use the full 16GB as one block.

---

**When the M60 Makes Sense**

- You're setting up **VMware Horizon / Citrix / GRID vGPU** virtual desktops
- You need a **cheap GPU for a server** and don't care about AI/ML
- You already have proper server cooling

**When to pass:**

- Any AI/ML workload — get the P100 instead
- Any workload needing large unified VRAM
- If the price is anywhere near P100 levels

---

**Bottom Line**

The M60 is a niche VDI card being sold with overstated claims. At the right price (~¥200–300 RMB range), it's fine for virtualization. But don't pay P100 prices for it, and ignore the "AI/rendering" marketing — that's just the seller casting a wide net.

---

References:

- [NVIDIA Tesla M60 Specs – TechPowerUp](https://www.techpowerup.com/gpu-specs/tesla-m60.c2760)
- [Tesla M60 vs P100 Compute Comparison – GPUpoet](https://gpupoet.com)
- [NVIDIA GRID M60 Datasheet – NVIDIA](https://images.nvidia.com/content/tesla/pdf/184427-Tesla-M60-DS-NV-Final-designleft.pdf)
