---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M60 $44 Price Reason
translated: false
type: note
---

Question: Why is an NVIDIA Tesla M60 16GB GPU being sold for only 320 CNY (~$44 USD) — is that price realistic?

Answer:

Yes, 320 CNY (~$44) is cheap, but it's not surprising for this card in 2026. Here's why:

**The M60 is genuinely old and limited for modern AI work:**
- Based on the **Maxwell architecture (GM204/GK210 — actually Maxwell, not Kepler)**, launched in **2015** — over 10 years old
- No support for **FP16 Tensor Cores** (those came with Volta, 2017)
- Limited to **CUDA Compute 5.2**, which many modern AI frameworks are dropping or have already dropped
- **PCIe only**, no NVLink for multi-GPU bandwidth
- Originally designed for **VMware vGPU / Citrix virtualization**, not training workloads

**Why supply is high and price is low:**
- Data centers are **mass-retiring** M60 cards as they upgrade to A100/H100/H200 generation hardware
- The Chinese used GPU market is flooded with ex-datacenter cards like M60, K80, P100
- 320 CNY is a typical **bulk/lot price** in Huaqiangbei or second-hand platforms (Xianyu/闲鱼) for this era of card

**What you actually get for 320 CNY:**
| Feature | Value |
|---|---|
| VRAM | 16GB GDDR5 (2×8GB dies) |
| FP32 Performance | ~7.4 TFLOPS |
| FP16 | Not accelerated |
| Power Draw | ~300W — needs proper power delivery |
| Driver Support | Still works on CUDA 11.x–12.x (with limitations) |

**Bottom line:** It's a legitimate bargain for **light inference, old-model fine-tuning, or VM virtualization** — but don't expect it to compete with even a used RTX 3090 for modern AI training. The price reflects its age and the flooded supply from retiring data centers.

---

References:
- [NVIDIA Tesla M60 Specs — TechPowerUp](https://www.techpowerup.com/gpu-specs/tesla-m60.c2760)
- [NVIDIA Tesla M60 Datasheet](https://images.nvidia.com/content/pdf/grid/data-sheet/nvidia-tesla-m60-datasheet.pdf)
