---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Between RTX 4070 and A6000
translated: false
type: note
---

**Question: what GPU is between RTX 4070 and RTX A6000 Pro?**

If you mean **AI / CUDA compute / LLM workload**, the ladder is roughly:

```
RTX 4070 12GB
      |
      |  (more VRAM / workstation)
      v
RTX 3080 Ti 12GB
RTX 3090 24GB
      |
      v
RTX A5000 24GB
      |
      v
RTX A5500 24GB
      |
      v
RTX A6000 48GB
```

([NVIDIA][1])

For your use case (LLM training, inference, ROCm experiments, local models), the interesting "middle" cards are:

| GPU       | VRAM           | Architecture       | AI value                     |
| --------- | -------------- | ------------------ | ---------------------------- |
| RTX 4070  | 12GB GDDR6X    | Ada                | Fast, but VRAM limited       |
| RTX 3090  | 24GB GDDR6X    | Ampere             | Best cheap AI card           |
| RTX A5000 | 24GB GDDR6 ECC | Ampere workstation | 3090 slower but professional |
| RTX A5500 | 24GB GDDR6 ECC | Ampere workstation | Between A5000/A6000          |
| RTX A6000 | 48GB GDDR6 ECC | Ampere workstation | Big model card               |

([NVIDIA][1])

### My recommendation for your situation

Since you already have:

* RTX 4070
* AMD MI50 16GB
* interested in GPT training / Qwen / local LLM

I would look at:

## 1. RTX 3090 24GB (best price/performance)

Probably the sweet spot.

Why:

* 2x VRAM of RTX 4070
* CUDA ecosystem
* can run:

  * 7B/14B/32B quant models easily
  * fine-tune small LLMs
  * LoRA on bigger models

The downside:

* 350W power
* used cards may have mining history

---

## 2. RTX A5000 24GB

A workstation version.

Advantages:

* ECC memory
* blower-style cards exist
* lower power (~230W)
* professional drivers

But:

For pure AI training:

```
RTX 3090 > RTX A5000
```

because 3090 has much higher compute.

---

## 3. RTX A6000 48GB

This is the real jump.

It is not "a little faster".

The important thing is:

```
RTX 4070:
12GB VRAM

RTX A6000:
48GB VRAM
```

4x memory capacity.

([NVIDIA][1])

You can move from:

```
Qwen 7B / 14B
        |
        v
Qwen 32B
        |
        v
70B quant inference
```

without multi-GPU tricks.

---

For your "one person lab" idea, I would rank:

```
Price/performance:
RTX 3090 24GB
        >
RTX A5000 24GB
        >
RTX A6000 48GB

Capability:
RTX A6000
        >
RTX 3090
        >
RTX 4070
```

The missing GPU between your RTX 4070 and A6000 is basically **RTX 3090 24GB**. It is the most common "AI hacker GPU". ([TechSpot][2])

For used-market prices, a rough target:

* RTX 3090: ¥4000-6000
* RTX A5000: ¥5000-8000
* RTX A6000: ¥8000-15000+

(depending heavily on China second-hand market).

[1]: https://www.nvidia.com/en-us/products/workstations/rtx-a6000/?utm_source=chatgpt.com "NVIDIA RTX A6000 For Powerful Visual Computing | NVIDIA"
[2]: https://www.techspot.com/specs/gpu/254404-nvidia-geforce-rtx-4070.html?utm_source=chatgpt.com "Nvidia GeForce RTX 4070 Specs | TechSpot"
