---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASRock RX 9070 XT Review
translated: false
type: note
---

**Question:** What is the ASRock Challenger Radeon RX 9070 XT, and is it worth considering?

**Answer:**

This is the **ASRock Challenger RX 9070 XT 16GB** — AMD's current-gen RDNA 4 flagship (below the 9070 XT's bigger siblings), priced at **$699.99** on Walmart via Newegg.

**Core specs:**

| Spec | Value |
|------|-------|
| GPU | Radeon RX 9070 XT (RDNA 4) |
| VRAM | 16GB GDDR6, 256-bit bus |
| Stream Processors | 4096 |
| Boost Clock | 2970 MHz |
| Interface | PCIe 5.0 x16 |
| Display outputs | 1× HDMI 2.1b, 3× DisplayPort 2.1a |
| Power draw | ~304W TDP (reference) |
| Dimensions | 3.9 in tall, 3.3 lb |

**What is this card?**

The RX 9070 XT is AMD's RDNA 4 architecture, launched in early 2025. RDNA 4 brings significant IPC uplifts over RDNA 3, improved ray tracing (2× RT throughput vs RDNA 3), hardware-accelerated AI inference units for FSR 4 (AMD's answer to DLSS 4), and a 256-bit bus with GDDR6 at competitive bandwidth. The "Challenger" is ASRock's entry-level cooler tier — dual/triple fan, functional but not premium like their Taichi or Phantom series.

**How it positions against alternatives:**

- **RTX 5070 ($599–629)** — DLSS 4 Multi Frame Generation is a big deal if you're NVIDIA-leaning; 12GB GDDR7 but narrower bus. For rasterization at 1440p/4K the 9070 XT trades blows.
- **RX 9070 (non-XT, ~$550–600)** — Same architecture, ~10–15% slower. If budget-constrained, the 9070 is excellent value.
- **RTX 5070 Ti (~$850–950)** — Notably faster, but costs significantly more.

At $699 the Challenger is the cheapest 9070 XT SKU (ASRock's own Taichi is $789, Steel Legend $749). It's basically a reference-cooler-tier board with a basic RGB strip. Reviews note it undervolts well for extra thermals/efficiency headroom.

**Relevance to your setup:**

You already have an RTX 4070 (12GB) on your Ubuntu workstation. The 9070 XT is ~35–45% faster in rasterization and has 16GB vs 12GB — meaningful if you're doing local inference or training (16GB fits larger models/batches). However: ROCm support on RDNA 4 (gfx1200/gfx1201) is still maturing as of mid-2026. If you're doing ML workloads on this card, verify ROCm 6.x compatibility with your target frameworks before buying — AMD's consumer cards have historically been finicky for compute vs gaming.

For pure gaming or a secondary display card it's a solid deal. For ML compute, the AMD MI300X you already have access to is orders of magnitude better, so this card would mainly be a gaming/display upgrade for your workstation.
