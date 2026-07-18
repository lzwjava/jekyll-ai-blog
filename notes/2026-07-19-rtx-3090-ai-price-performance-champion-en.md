---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3090 AI Price-Performance Champion
translated: false
type: note
---

Question: Read and analyze the article about RTX 3090 becoming a cost-effective AI GPU.

Answer:

The article is titled **“A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王”** (“Nobody buys AMD cards! Five-year-old NVIDIA card becomes popular again: used RTX 3090 is the king of price/performance”). ([MyDrivers News][1])

The main argument:

* **RTX 3090 (2020 Ampere)** is still attractive in 2026 for local AI workloads because:

  * 24GB VRAM
  * mature CUDA ecosystem
  * good FP16/BF16 Tensor Core support
  * cheap used market
* The article argues that newer GPUs often have better compute but worse price/VRAM ratio for AI. ([MyDrivers News][1])

Key points:

### 1. For AI, VRAM > raw FLOPS

This is the most important point.

For LLM:

```
model size ≈ parameters × bytes per parameter
```

Examples:

FP16:

```
7B model:
7B × 2 bytes ≈ 14GB

14B model:
14B × 2 bytes ≈ 28GB
```

So:

RTX 4070 Ti:

```
12GB
```

RTX 4070:

```
12GB
```

RTX 3090:

```
24GB
```

The 3090 can load models that simply cannot fit on 12GB cards.

For your use case:

* Qwen
* Llama
* fine-tuning
* LoRA
* local agents

24GB is a huge jump.

---

### 2. Why CUDA beats AMD ROCm here

The article's strongest point is software ecosystem. ([MyDrivers News][1])

NVIDIA:

```
PyTorch
 ↓
CUDA
 ↓
cuBLAS
 ↓
TensorRT
 ↓
vLLM
 ↓
FlashAttention
```

AMD:

```
PyTorch
 ↓
ROCm
 ↓
HIP
 ↓
compatibility issues
```

ROCm has improved a lot, but the long tail is still weaker.

For example:

A random GitHub repo:

```
pip install xxx
python train.py
```

NVIDIA:
usually works.

AMD:
maybe:

```
change CUDA -> HIP
patch kernel
compile xformers
disable flash attention
```

For someone experimenting daily, this friction matters.

---

### 3. Why RX 7900 XTX / 7900 XT is less attractive for AI

The article compares RTX 3090 with RX 7900 XTX. ([MyDrivers News][1])

Hardware:

RX 7900 XTX:

```
24GB VRAM
very strong gaming
```

RTX 3090:

```
24GB VRAM
CUDA
Tensor cores
```

For gaming:

```
7900 XTX > 3090
```

For AI:

```
3090 >>> 7900 XTX
```

because software dominates.

---

### 4. The article exaggerates a little

The "king" statement is marketing.

RTX 3090 has weaknesses:

#### Power

```
RTX 3090:
350W+
```

Two cards:

```
700W+
```

You need:

* good PSU
* cooling
* motherboard spacing

#### No FP8 / newer Tensor features

Newer Ada/Blackwell:

```
RTX 4090
RTX 5090
```

have much better efficiency.

#### Used card risk

Many 3090s were:

* crypto mining cards
* 24/7 loaded
* thermal cycled

Need testing:

```
nvidia-smi
GPU memory test
OCCT VRAM test
long inference test
```

---

### My view for your AI training setup

Given your history:

* RTX 4070 12GB
* trained GPT-2 124M
* interested in LLM fine-tuning
* local inference

I think RTX 3090 is actually one of the few upgrades that make sense.

Upgrade:

```
RTX 4070 12GB
        |
        v
RTX 3090 24GB
```

is more meaningful than:

```
RTX 4070
        |
        v
RTX 5070
```

because VRAM doubles.

Your workflow changes:

Before:

```
Qwen 7B quantized
small LoRA
```

After:

```
Qwen 14B quantized
larger LoRA
24GB inference
bigger batch size
```

---

My ranking for local AI around this price:

| GPU               | VRAM | AI value            |
| ----------------- | ---- | ------------------- |
| RTX 3090          | 24GB | ⭐⭐⭐⭐⭐               |
| RTX 4090          | 24GB | ⭐⭐⭐⭐⭐ but expensive |
| RTX 4070 Ti Super | 16GB | ⭐⭐⭐                 |
| RX 7900 XTX       | 24GB | ⭐⭐                  |
| RX 9070 XT        | 16GB | ⭐⭐                  |
| RTX 4070          | 12GB | ⭐⭐                  |

For an AI engineer, **RTX 3090 is probably the last "cheap VRAM monster" before prices jump to workstation/datacenter territory.**

The article's conclusion is directionally correct: **AI workloads changed the GPU market. A five-year-old 24GB card can beat a newer 12–16GB card simply because the model fits.** ([MyDrivers News][1])

References:

* 快科技: 《A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王》 ([MyDrivers News][1])

[1]: https://news.mydrivers.com/1/1109/1109956.htm "A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王--快科技--科技改变未来"
