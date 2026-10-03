---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 唯一超过24GB的消费级GPU
translated: true
type: note
---

问题：哪些面向消费者的英伟达显卡拥有超过 24 GB 的显存？

答案：

唯一一款显存超过 24 GB 的主流消费级显卡是 **GeForce RTX 5090**。它配备了 32 GB 的 GDDR7 显存，位宽为 512-bit，带宽高达 1,792 GB/s。相比 RTX 4090（32 GB vs 24 GB），显存容量提升了 33%，是目前显存最高的消费级 GPU。

- **RTX 5090（32 GB）：** 唯一一款显存超过 24 GB 的消费级 GeForce 显卡。其官方建议零售价为 1,999 美元，但供货有限且需求旺盛。
- **显存为 24 GB 或以下的显卡：** RTX 4090 和 RTX 3090 拥有 24 GB 显存。RTX 5080 和 5070 Ti 为 16 GB，RTX 5070 为 12 GB。
- **超过 32 GB：** 超过 32 GB 则没有主流的 GeForce 选项。像 48 GB 或 96 GB 这样的容量来自于英伟达的专业产品线（例如，据 Tom's Hardware 报道，RTX Pro 6000 拥有 96 GB 显存）。这些是工作站显卡，而非消费级显卡，且价格昂贵得多。
- **改装显卡：** 存在一些改装版 RTX 5090，显存高达 128 GB，但有一款被描述为“超限量”原型机，售价高达 13,000 美元。这些并非官方或实用的消费级选择。

32 GB 在实际使用中的适用情况：8B 模型在 FP16 下（约 16 GB），以及 32B 模型在 Q4/AWQ 下（约 20 GB）。4-bit 的 Llama 3 70B（约 38 GB）仍然无法单卡运行。

我在搜索中未发现更新款的超过 32 GB 的消费级 GPU，但新产品的发布随时可能出现，因此建议查看英伟达官网了解最新产品线。

参考文献：

- [NVIDIA RTX 5090: Specs, 32GB VRAM & AI Benchmarks (2026)](https://www.runpod.io/articles/guides/nvidia-rtx-5090)
- [NVIDIA RTX 5090 Specs: 32GB GDDR7, 1,792 GB/s, FP4 Tensor](https://www.spheron.network/blog/nvidia-rtx-5090-specs/)
- [NVIDIA GeForce RTX 5090: Everything You Need to Know](https://vast.ai/article/nvidia-geforce-rtx-5090-specs-everything-you-need-to-know)
- [Configure a PC with NVIDIA GeForce RTX 5090 32GB (Puget Systems)](https://www.pugetsystems.com/parts/Video-Card/NVIDIA-GeForce-RTX-5090-32GB-16123/)
- [Upgraded Nvidia RTX 5090 gets 128GB VRAM (Tom's Hardware)](https://www.tomshardware.com/pc-components/gpus/upgraded-nvidia-rtx-5090-gets-128gb-vram-and-usd13-000-price-tag-super-limited-gpu-is-described-as-a-prototype)
- [RTX 5090 vs RTX 3090: Is 32GB Worth the Upgrade?](https://gigagpu.com/rtx-5090-vs-rtx-3090/)