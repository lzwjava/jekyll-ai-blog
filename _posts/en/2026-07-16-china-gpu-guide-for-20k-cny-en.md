---
audio: false
generated: true
image: false
lang: en
layout: post
title: China GPU Guide for 20K CNY
translated: false
type: note
---

Question: Best GPU option in China for a 20k CNY budget, primarily for local LLM training/inference work.

Answer:

Given your workload (LLM training/inference, agent dev, not gaming), **VRAM and $/GB beat raw compute**. Here's what actually fits 20k CNY right now (July 2026 China market):

**Best pick: 2x RTX 3090 24GB (used) — ~11-14k CNY**
- personal-use RTX 3090s on Xianyu have been going for around 7,000 CNY each recently, up from ~5,000 CNY a month prior — so budget ~10-14k CNY for a matched pair depending on timing.
- 48GB total VRAM across two cards, GDDR6X, 384-bit bus with 936GB/s bandwidth per card — enough to load 70B models in 4-bit or do QLoRA on 13B-34B comfortably.
- Mature CUDA/driver stack, no modded firmware risk, proven for training (this is literally what half the local-LLM crowd on Xianyu is running).
- for edge AI, 24GB+ VRAM and price matter more than raw compute, and 3090 fits that better than newer cards at similar cost.
- Downside: no NVLink bridge on most 3090 non-Ti models sold at consumer price (some do have it — check before buying), so multi-GPU means PCIe-only tensor/pipeline parallelism (fine for inference, slower for some training setups).

**Alternative: single RTX 4090D 48GB (VRAM-modded) — ~19-20k CNY**
- these are sold as "48GB for DeepSeek" modded 4090D turbo cards around $2,599-2,759, i.e. ~18.7-19.8k CNY — right at your ceiling.
- One card, one PCIe slot, 48GB VRAM — good if you're inference-heavy and want simplicity over a dual-GPU rig.
- Real risk: these are hand-modded (Hynix/Samsung chips reballed onto 4090D PCBs), no official Nvidia support, some batches have VRAM instability under sustained load. Buy from a seller with return window, stress-test immediately (`nvidia-smi -q -d MEMORY` + long `torch` training loop to catch ECC errors).

**Skip: RTX 5090D V2** — GDDR7 shortage has pushed street price to ~32,000-34,000 CNY, more than 1.5x your budget for a card whose extra compute you won't fully use if you're VRAM-bound anyway.

**My call**: 2x 3090 if you're doing any training (fine-tuning, small pretraining runs like your GPT-2 work) — PCIe multi-GPU is a solved problem in your stack already. Single 4090D 48GB if you're mostly serving/inference and want to avoid multi-GPU orchestration overhead.

References:
- [显卡日报: 二手RTX 3090价格暴涨 - 知乎](https://zhuanlan.zhihu.com/p/664780612)
- [A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王 - 快科技](https://news.mydrivers.com/1/1109/1109956.htm)
- [RTX 4090D 48GB modded listings - Alibaba](https://www.alibaba.com/countrysearch/CN/4090.html)
- [RTX 5090 D V2 price surge to 34,000 CNY - XIKII UPLINK](https://m.xikii.com/uplink/post/9280)
