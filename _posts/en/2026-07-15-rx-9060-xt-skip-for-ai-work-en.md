---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RX 9060 XT: Skip for AI Work"
translated: false
type: note
---

Question: What is the Sapphire RX 9060 XT 16GB (METAL alloy design) card, and is it any good for LLM/AI work?

Answer:

This is a gaming-segment card, not a real AI compute card — worth being clear about that upfront given your use case (GPT-2 training on MI300X, agent inference).

**Silicon**

- GPU: Navi 44 XT, RDNA 4 architecture, 4nm, 199mm², 29.7B transistors
- 2048 stream processors, 32 ray tracing cores, 64 "tensor cores" (AMD's marketing term for RDNA4's matrix/WMMA units — not comparable to Nvidia Tensor Cores in software ecosystem maturity)
- Full PCIe 5.0 x16 host interface, versus PCIe Gen 4 8-lane on the prior RX 7600

**Memory**

- 16GB GDDR6 over a 128-bit bus, 320 GB/s bandwidth

**Clocks / power (Pulse variant, this "METAL" cooler)**

- Game clock 2700 MHz, boost clock up to 3290 MHz, memory clock 2500 MHz (20 Gbps effective)
- 170W typical board power, single 8-pin connector, 24cm length, two slots thick

**Price/positioning**

- AMD's MSRP is $349 for 16GB (8GB variant is $299). Sapphire's Pulse OC model is priced around $365. "METAL" (金属脉动) is just Sapphire's Chinese-market marketing name for the Pulse's cooler shroud/backplate — same silicon as the international Pulse SKU.

**For your actual workloads — verdict: skip it.**

- 320 GB/s bandwidth and no CUDA means ROCm/HIP is your only path, and RDNA4 consumer card ROCm support is patchy compared to your MI300X (which has proper CDNA3 + full ROCm/ HIP stack + way more HBM3 bandwidth).
- 16GB VRAM only gets you small local inference (7B Q4 quant territory), not anything near your GPT-2 760M training use case at real batch sizes.
- The "DeepSeek AI" / "人工智能" labeling in Chinese retail listings is just marketing riding the DeepSeek wave — this card has zero special DeepSeek optimization; it's identical hardware to the global Pulse 16GB SKU.

If you want a cheap local-inference box for llama.cpp/vLLM experiments this is a fine $349 gaming card that happens to have 16GB VRAM. If you're evaluating it as a training node, don't — stick with your MI300X or rent cloud compute.

References:

- [SAPPHIRE PULSE Radeon RX 9060 XT 16G GDDR6](https://www.sapphiretech.com/en/consumer/pulse-radeon-rx-9060-xt-16g-gddr6)
- [SAPPHIRE RX 9060 XT 16GB PULSE spec database](https://videocardz.net/sapphire-radeon-rx-9060-xt-16gb-pulse)
- [TechPowerUp: Sapphire RX 9060 XT Pulse OC 16GB Review](https://www.techpowerup.com/review/sapphire-radeon-rx-9060-xt-pulse-oc/)
- [PC Perspective: RX 9060 XT 16GB Sapphire PULSE Review](https://pcper.com/2025/06/amd-radeon-rx-9060-xt-16-gb-review-sapphire-pulse-tested/)
