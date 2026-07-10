---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA V100 GPU Overview
translated: false
type: note
---

Question: what's V100?

Answer:

NVIDIA Tesla V100 (usually called **V100**) is a **2017 NVIDIA data center AI GPU** based on the **Volta architecture**. It was one of the first GPUs with dedicated **Tensor Cores**, designed for deep learning training and HPC. ([NVIDIA][1])

Think of it as the ancestor of today's A100/H100.

Architecture timeline:

```
Tesla P100 (Pascal, 2016)
        |
Tesla V100 (Volta, 2017)  <-- Tensor Core era starts
        |
A100 (Ampere, 2020)
        |
H100 (Hopper, 2022)
```

Main specs:

```
GPU:              GV100
Architecture:     Volta
CUDA cores:       5120
Tensor cores:     640
VRAM:             16GB / 32GB HBM2
Memory bandwidth: ~900 GB/s
Power:            250W PCIe / 300W SXM
Compute:          sm_70
```

([NVIDIA Images][2])

The important part for AI:

### 1. HBM2 memory

Unlike RTX cards:

```
RTX 4070:
12GB GDDR6X
~500 GB/s bandwidth

V100:
16/32GB HBM2
~900 GB/s bandwidth
```

HBM is much faster memory, which helps large matrix operations.

### 2. Tensor Cores

V100 introduced NVIDIA Tensor Cores:

```
normal CUDA cores:
    FP32 multiply/add

Tensor Core:
    matrix multiply accumulate

    A @ B + C
```

Deep learning is mostly:

```
Y = XW
```

large matrix multiplications, so Tensor Cores accelerate training/inference. ([arXiv][3])

### Compared with your RTX 4070

Roughly:

|                  | V100         | RTX 4070     |
| ---------------- | ------------ | ------------ |
| Year             | 2017         | 2023         |
| Architecture     | Volta        | Ada          |
| VRAM             | 16/32GB HBM2 | 12GB GDDR6X  |
| Tensor cores     | 1st gen      | 4th gen      |
| CUDA cores       | 5120         | 5888         |
| FP16 AI          | good         | much better  |
| VRAM size        | advantage    | disadvantage |
| Software support | older        | newer        |

For modern LLM work:

* **Training small models** → V100 still works.
* **Running large models because VRAM matters** → V100 32GB is interesting.
* **Modern CUDA / FlashAttention / FP8 / newest frameworks** → RTX 4070 wins.

The biggest issue is software compatibility. V100 is **compute capability 7.0**, while many new AI optimizations target Ampere+ (sm80+) or Hopper. ([Reddit][4])

### V100 vs your MI50

Your AMD MI50 comparison is interesting:

```
MI50:
- 16GB HBM2
- ~1TB/s bandwidth
- 300W
- ROCm ecosystem

V100:
- 16/32GB HBM2
- ~900GB/s
- 250-300W
- CUDA ecosystem
```

Hardware is similar era, but CUDA support makes V100 much easier for PyTorch.

A cheap V100 today is basically a "data center relic" that can still do useful AI work because **VRAM + bandwidth age better than raw FLOPS**. ([Reddit][5])

For your use case (nanoGPT/GPT-2 style training), a V100 32GB would actually be a very capable experimental card, but your RTX 4070 has the advantage of modern CUDA kernels and lower friction.

[1]: https://www.nvidia.com/en-in/data-center/v100/?utm_source=chatgpt.com "NVIDIA V100 | NVIDIA"
[2]: https://images.nvidia.com/content/technologies/volta/pdf/tesla-volta-v100-datasheet.pdf?utm_source=chatgpt.com "NVIDIA V100"
[3]: https://arxiv.org/abs/1803.04014?utm_source=chatgpt.com "NVIDIA Tensor Core Programmability, Performance & Precision"
[4]: https://www.reddit.com/r/LocalLLM/comments/1tx6emj/v100_question/?utm_source=chatgpt.com "v100 question"
[5]: https://www.reddit.com/r/RigBuild/comments/1t9xeyj/nvidias_v100_an_8year_old_gpu_now_sells_for_100/?utm_source=chatgpt.com "NVIDIA’s V100, An 8-Year Old GPU, Now Sells for $100 and Crushes Modern Consumer Cards in AI LLM Workloads"
