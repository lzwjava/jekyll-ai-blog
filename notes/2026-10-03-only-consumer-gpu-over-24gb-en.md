---
audio: false
generated: true
image: false
lang: en
layout: post
title: Only Consumer GPU Over 24GB
translated: false
type: note
---

Question: Which NVIDIA GPU cards for consumers have more than 24 GB of VRAM?

Answer:

The only mainstream consumer card with more than 24 GB is the **GeForce RTX 5090**. It has 32GB of GDDR7 memory on a 512-bit bus, delivering 1,792 GB/s of bandwidth. That is 33% more VRAM than the RTX 4090 (32GB vs 24GB), and it is the consumer GPU with the highest available VRAM.

- **RTX 5090 (32 GB):** The only consumer GeForce card above 24 GB. Its official MSRP started at $1,999, but availability has been limited and demand strong.
- **Cards at 24 GB or below:** The RTX 4090 and RTX 3090 have 24 GB. The RTX 5080 and 5070 Ti have 16 GB, and the RTX 5070 has 12 GB.
- **Above 32 GB:** Beyond 32 GB there is no mainstream GeForce option. Capacities like 48 GB or 96 GB come from NVIDIA's professional line (for example, the RTX Pro 6000 with 96 GB, per Tom's Hardware). Those are workstation cards, not consumer cards, and are much more expensive.
- **Modded cards:** Some modded RTX 5090s with up to 128 GB exist, but one was described as a "super limited" prototype with a $13,000 price tag. These are not an official or practical consumer option.

What 32 GB fits in practice: 8B models at FP16 (~16GB), and 32B models at Q4/AWQ (~20GB). A 4-bit Llama 3 70B (about 38 GB) still does not fit on one card.

I did not find a newer consumer GPU above 32 GB in my search, but new releases can appear, so it is worth checking NVIDIA's site for the latest lineup.

References:
- [NVIDIA RTX 5090: Specs, 32GB VRAM & AI Benchmarks (2026)](https://www.runpod.io/articles/guides/nvidia-rtx-5090)
- [NVIDIA RTX 5090 Specs: 32GB GDDR7, 1,792 GB/s, FP4 Tensor](https://www.spheron.network/blog/nvidia-rtx-5090-specs/)
- [NVIDIA GeForce RTX 5090: Everything You Need to Know](https://vast.ai/article/nvidia-geforce-rtx-5090-specs-everything-you-need-to-know)
- [Configure a PC with NVIDIA GeForce RTX 5090 32GB (Puget Systems)](https://www.pugetsystems.com/parts/Video-Card/NVIDIA-GeForce-RTX-5090-32GB-16123/)
- [Upgraded Nvidia RTX 5090 gets 128GB VRAM (Tom's Hardware)](https://www.tomshardware.com/pc-components/gpus/upgraded-nvidia-rtx-5090-gets-128gb-vram-and-usd13-000-price-tag-super-limited-gpu-is-described-as-a-prototype)
- [RTX 5090 vs RTX 3090: Is 32GB Worth the Upgrade?](https://gigagpu.com/rtx-5090-vs-rtx-3090/)
