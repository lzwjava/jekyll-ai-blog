---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX Pro 6000 Rental Earnings
translated: false
type: note
---

**Question:** If I rent out an NVIDIA RTX A6000 Pro (92GB VRAM) to others on RunPod or similar platforms, what's the earning potential and setup?**Answer:**

First, clarifying the GPU — you said "A6000 Pro 显卡, 92GB." That's almost certainly the **NVIDIA RTX Pro 6000 Blackwell** (96GB GDDR7), not the older RTX A6000 (48GB). Here's the full picture:

---

## The GPU: RTX Pro 6000 Blackwell

It features 96GB of GDDR7 ECC VRAM, 24,064 CUDA cores, 1,792 GB/s memory bandwidth, and 5th-gen Tensor Cores with FP4 support. MSRP launched at ~$8,565 in March 2025, but as of June 2026, Nvidia has raised it to $13,250 — a 55% hike in one year. It's the **largest VRAM single workstation GPU** you can buy, outside of datacenter HBM SKUs (H100/H200/B200).

---

## Rental Market Rates (as of June 2026)

| Platform | Rate |
| --- | --- |
| **Vast.ai** (Workstation Edition) | ~$1.20/hr |
| **Vast.ai** (Server Edition) | ~$1.40/hr |
| **RunPod** | ~$1.27–2.00/hr |
| **Spheron** | ~$2.35/hr |
| **Google Cloud** | ~$4.50/hr |

Market median is $1.27/hr across 125 available configurations, with a floor around $0.67/hr.

---

## Revenue Potential (if you host it)

At $1.20–1.40/hr (Vast.ai community cloud rate, which is what you'd earn as a host):

| Utilization | Daily | Monthly |
| --- | --- | --- |
| 30% | ~$8–10 | ~$250–300 |
| 60% | ~$17–20 | ~$500–600 |
| 90% | ~$26–30 | ~$780–900 |

This is **much better than a 4070** because:

- 96GB VRAM is a sweet spot for 70B FP8 inference (Llama 3.3 70B, Qwen 72B), which is in high demand
- It can run Llama 3.3 70B FP8, Qwen 2.5 32B FP16, and 70B AWQ models comfortably on a single GPU — use cases that have no single-GPU alternative below H100 pricing
- Renters are willing to pay $1–2/hr rather than $1.50+/hr for H100

---

## Key Constraint: Workstation vs Server Edition

NVIDIA offers two versions: the Workstation Edition (for desktops) and the Server Edition (passive cooling, for data centers). They share the same architecture, VRAM, and core count but are designed for different environments.

If you have the **Workstation Edition** (active fan cooled), it's harder to host in a multi-GPU rack but fine for a single-machine setup. The **Server Edition** is what clouds prefer.

Also critical: the RTX Pro 6000 lacks NVLink support, so multi-GPU tensor parallelism is off the table. That limits it to single-GPU workloads only.

---

## Should You Host It on Vast.ai or RunPod?

**Vast.ai** is better for hosting your own hardware:

- Better marketplace for community/indie hosts
- More utilization from cost-sensitive researchers who need 96GB but won't pay H100 rates
- Vast.ai lists the Server Edition at ~$1.40/hr and the Workstation Edition at ~$1.20/hr

**RunPod Community Cloud** is an option too, but RunPod is more curated and mostly their own DC hardware. Home hosts get lower priority in their scheduling.

---

## Verdict for You

Given you have an RTX 4070 at `192.168.x.x` — if you're **considering buying an RTX Pro 6000 Blackwell** and hosting it, the math at 60% utilization is ~$500–600/month gross. But:

- Hardware costs $11k–13k now (MSRP inflated massively)
- Power: 600W TDP → ~$50–80/month electricity cost
- Break-even at 60% utilization: **18–22 months**
- Risk: GPU pricing crashes, or B200/GB200 flood the market

If you **already own** one, hosting it is a no-brainer — list it on Vast.ai today and make $300–800/month depending on demand.

**References:**

- [Thunder Compute — RTX Pro 6000 Pricing June 2026](https://www.thundercompute.com/blog/nvidia-rtx-pro-6000-pricing)
- [Vast.ai — RTX PRO 6000 WS pricing](https://vast.ai/pricing/gpu/RTX-PRO-6000-WS)
- [getdeploying.com — RTX Pro 6000 cloud price comparison](https://getdeploying.com/gpus/nvidia-rtx-pro-6000)
- [MLQ News — Nvidia raises RTX Pro 6000 MSRP to $13,250](https://mlq.ai/news/nvidia-raises-rtx-pro-6000-blackwell-msrp-to-13250-a-55-hike-in-one-year/)
