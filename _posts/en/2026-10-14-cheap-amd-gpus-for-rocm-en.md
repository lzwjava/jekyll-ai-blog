---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheap AMD GPUs for ROCm
translated: false
type: note
---

## Question: Which cheap second-hand AMD GPUs support ROCm?

**Answer:** For your AI lab, I'd focus on older AMD Instinct accelerators rather than consumer Radeon cards. But there's a catch: **the cheapest AMD GPU with enough VRAM is not necessarily the cheapest GPU that can run PyTorch with ROCm reliably.**

My shortlist to investigate:

| GPU | VRAM | Architecture | Assessment |
| --- | ---: | --- | --- |
| Radeon RX 6600 | 8GB | RDNA 2 | Cheap consumer card; check exact ROCm support |
| Radeon RX 6700 XT | 12GB | RDNA 2 | More VRAM, but software support needs verification |
| Radeon RX 6800 | 16GB | RDNA 2 | Potentially interesting for budget AI |
| Instinct MI50 | 16GB or 32GB | CDNA 1 | Older compute accelerator; modern ROCm support is a concern |
| Instinct MI100 | 32GB | CDNA 1 | More promising for compute, but check current support and used prices |
| Instinct MI210 | 64GB | CDNA 2 | Better modern compute option, usually more expensive |

These are candidates to investigate, not a claim that every card is supported by the latest ROCm release.

## 1. My top picks

### Option A: Instinct MI100 32GB — for compute

The MI100 is the most interesting older workstation/server accelerator to investigate if you want substantial VRAM at a low price.

- 32GB HBM2
- 1 TB/s memory bandwidth
- CDNA architecture, target `gfx908`
- Listed in AMD's current ROCm hardware support documentation. [AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

Its main disadvantages are 300W power consumption, server-oriented hardware, and potentially difficult installation. Check the exact ROCm/PyTorch combination before purchasing.

### Option B: Radeon RX 7900 XT 20GB — for a consumer PC

If you prefer a normal gaming GPU, the RX 7900 XT is worth investigating.

- 20GB GDDR6
- RDNA 3 architecture
- Supported by current ROCm documentation. [AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

It is newer and more practical than the MI100 for a conventional desktop, although used prices may be higher.

### Option C: Radeon Pro W6800 32GB — for VRAM capacity

The W6800 offers 32GB of VRAM and appears in AMD's current ROCm support documentation. [AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

It is worth comparing against the MI100 if you find one cheaply, particularly if you want a workstation card rather than a server accelerator.

## 2. What about the really cheap MI50 and RX 6800?

Be careful with these two.

- **MI50 32GB:** Attractive memory capacity, but community reports identify ROCm 6.3.3 as the last compatible release. Treat it as a legacy-software project rather than a current ROCm solution. [Reddit](https://www.reddit.com/r/ROCm/comments/1ominy2?utm_source=chatgpt.com)
- **RX 6800 16GB:** It appears in older ROCm hardware documentation, but it is absent from the current ROCm 10.1 list of officially supported Radeon GPUs. I would not buy one specifically for current official ROCm support. [AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

## 3. What I'd do in your position

Since you already have an RTX 4070 12GB and are exploring inexpensive GPUs for LLM experiments, I'd compare these three:

| GPU | Primary advantage | Recommendation |
| --- | --- | --- |
| MI100 32GB | Large HBM capacity | Best candidate for a cheap compute accelerator |
| Radeon Pro W6800 32GB | Large VRAM in a workstation card | Worth investigating |
| RX 7900 XT 20GB | Modern consumer GPU | Better desktop-oriented option |

**One question: Are you buying in China's second-hand market, such as Xianyu, or in the US?** That changes which card I'd recommend because local used prices can completely change the value ranking.
