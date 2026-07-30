---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AMD RX 9060 XT: Naming Clarified"
translated: false
type: note
---

**Question:** What's the AMD RX 9600 XT GPU?

**Answer:** There's a naming mixup worth flagging first — "RX 9600 XT" was the pre-launch leaked codename; AMD officially shipped it as the **RX 9060 XT** at Computex 2025. No retail card is actually branded "9600 XT." (Some of the search results above — the ones citing 12GB GDDR7, 750GB/s bandwidth, or 0.25GB GDDR5 — are garbage/AI-generated spam pages, ignore those.)

Real specs for the RX 9060 XT (RDNA 4, Navi 44):

| Spec | Value |
|---|---|
| Process | TSMC N4P (4nm) |
| Transistors | 29.7B |
| Compute Units | 32 |
| Base / Boost clock | 2530 MHz / 3130 MHz |
| Memory | 8GB or 16GB GDDR6 |
| Target segment | 1080p/1440p gaming, competes with RTX 5060 Ti |
| MSRP | $299 (8GB) / $349 (16GB) |

For your use case (local inference / small fine-tunes), the **16GB variant is the only one worth considering** — 8GB is a non-starter for anything beyond toy models. Even at 16GB, this is a gaming card: no tensor cores equivalent, ROCm support for RDNA4 consumer cards is still maturing (worth checking ROCm compatibility matrix before buying if you plan to run PyTorch/vLLM on it — CUDA-only stacks obviously won't work at all).

Given you're already on MI300X for real training work, this card only makes sense as a cheap local dev/inference box, not a training node.

**References:**
- [AMD Radeon RX 9600 XT Launched (Navi 44) - Geeks3D](https://www.geeks3d.com/20250521/amd-radeon-rx-9060-xt-announced-navi-44/)
- [AMD RX 9060 XT leaked specs - Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/amd-rx-9060-xt-leaked-specs-allege-speedy-3-3-ghz-gpu-clock)
