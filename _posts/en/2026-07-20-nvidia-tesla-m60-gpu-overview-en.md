---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia Tesla M60 GPU Overview
translated: false
type: note
---

Question: Intro to NVIDIA Tesla M60 16GB GPU (used card, ¥288)

Answer:

![Image](https://images.openai.com/static-rsc-4/cvlA10JHDuWSJJh6f0x9BzQZkmFeN9chOCFwRX2-jCGJQ9lY7g7SckIe8lGsEb4A6gTqqGd7SUa_pORJ8TXX8a88Jkh1AeKBIpaPd7pMJaZ1C2T-D0xfcqpQUDDnSbhmSdFiAzwVAD7PvI1QvYxCDA2ZmrqyWdrKFh3SJ3IbVWhQZ39BBIx34RvhmWC3d1tU?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/q4XKceLqIeA624foJ5QlqYUFhIffVgot7JU3ku8lDpUhby_2WiprAbxRyEacM5lLPmguuWhrLxJb3F-WQqkuz7nEJiGBoL8C0x4x9a6GYZIGH6Kcs3agiGzae83QdRjd1ptKjmmMWBm-aQfQp0bYi2bHc5Aj8AvAMo7Acl-YxAoMqlrNpajCMoQ9h7iGyIsW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/I3U46S-PS4cekwLOsraO7j7UMMwX_aHS6GZxyEdHNxsIpUl11dduXAlbATpDyVtMXW1lV8WzBic62FEAyMyAfultp0rDF1LXNyAI_c6QX8WCuGh9uZHPrRZxLejpskDfaHtNHvumxDtPPbL1Qg1IN-GTfNyRfpfpyU2OfcKDXQJjbEW32yHxqrirhu--gDv7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/VJVR2FyJE-p1mEc6wEfHkD6T4_ZFCms69ALL18ILL50dAChsRWigYg6Dl9oN7FPKpFQHdkn51oVcd4GVUzSoYmp7DBsU4CIHtOqH5mMNZT_6_MOfLpRK_VhMSLcPyfwSxDoDWeNdteW0s54nNleVZq0GcvYGvqqWxPM1SIfVFVUFzdYFTjx_buw_N6TgYNfv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NNggD1TlST0HNYUm4S84wxkf9l8zYoaRjunhpgJvPr5ZRMKSH7SMggmF128lMGCnlIsMx04tJ039O8R-cZGrPksGYWTl-jllW-9uds-Y8m8mrwQbVKoMA8djmHWDL92pmWlokfytHut1KsuyodgYWxnYMtWdIc44GFwxUcugfCocuHB9jCW8VQeSZQ7-b8_2?purpose=fullsize)

This is **NVIDIA Tesla M60**, a data-center GPU from the **Maxwell generation (2015)**. It is a special card because it is basically **two GPUs on one PCB**.

### Basic specs

| Item         | Tesla M60                                 |
| ------------ | ----------------------------------------- |
| Architecture | Maxwell (GM204)                           |
| Release      | 2015                                      |
| GPU cores    | 2 × GM204 GPUs                            |
| VRAM         | 16GB total (2 × 8GB GDDR5)                |
| Memory bus   | 2 × 256-bit                               |
| PCIe         | PCIe 3.0 x16                              |
| TDP          | ~300W                                     |
| FP32 compute | ~9 TFLOPS                                 |
| Form factor  | Dual-slot, passive server card originally |

Important: **16GB does NOT mean one GPU has 16GB.**

It is:

```
Tesla M60
 ├── GPU #1
 │    └── 8GB VRAM
 │
 └── GPU #2
      └── 8GB VRAM
```

The two GPUs do not combine memory automatically.

---

## What was Tesla M60 designed for?

Main purpose:

* VDI (Virtual Desktop Infrastructure)
* Cloud gaming
* Virtual workstation
* NVIDIA GRID

For example:

```
One M60
 |
 +-- VM 1 → GPU slice
 |
 +-- VM 2 → GPU slice
 |
 +-- VM 3 → GPU slice
```

It was popular in cloud providers around 2015-2020.

---

## AI / LLM usage today

For AI training/inference:

### Good:

✅ CUDA works
✅ PyTorch can run
✅ 16GB total VRAM (if using both GPUs separately)
✅ Very cheap

### Bad:

❌ Old Maxwell architecture
❌ No Tensor Cores
❌ No BF16
❌ No FP16 acceleration like modern RTX cards
❌ Very slow compared with RTX 3060/3090/4070

Performance comparison:

| GPU           |       FP32 |
| ------------- | ---------: |
| Tesla M60     |  ~9 TFLOPS |
| RTX 3060 12GB | ~13 TFLOPS |
| RTX 4070      | ~29 TFLOPS |
| RTX 3090      | ~36 TFLOPS |

For LLM:

```
M60 16GB
≈ two slow 8GB GPUs

RTX 3090 24GB
≈ modern AI workstation card
```

A single RTX 3090 is massively faster.

---

## Compatibility issues

This card has some traps.

### 1. Power

It needs:

```
PCIe slot
+
2 × 8-pin power
```

Your listing says it includes power cable, so likely OK.

### 2. Cooling

Many M60 cards are **passive**:

```
server airflow required
```

They expect a high-pressure server fan.

A normal desktop case may overheat.

The seller includes a fan, which is important.

### 3. Driver support

Modern NVIDIA drivers still support Maxwell, but:

* CUDA 12 dropped some old architectures
* newer PyTorch builds may not support it well

You may need:

```
CUDA 11.x
PyTorch older versions
```

---

## At ¥288 CNY, is it worth it?

Depends on purpose.

### Good buy:

✅ CUDA experiment
✅ learn multi-GPU programming
✅ cheap GPU cluster experiments
✅ CUDA kernel development
✅ old workstation

### Not recommended:

❌ LLM training
❌ fine-tuning Qwen/Llama models
❌ replacing RTX 4070
❌ building AI workstation

For comparison:

```
Tesla M60 ¥288
↓
16GB VRAM

RTX 3060 12GB used ~¥1200-1500
↓
much faster

RTX 3090 24GB used ~¥2500-3500
↓
AI monster
```

For your AI experiments (nanoGPT, Qwen, agents), I would rank:

```
RTX 3090 24GB
    >
RTX 4090
    >
RTX 4070 12GB
    >
RTX 3060 12GB
    >
Tesla M60
```

The M60 is more like a **GPU museum piece / CUDA playground**, not an AI training card.

References:

* NVIDIA Tesla M60 product overview: [https://www.nvidia.com/en-us/data-center/tesla-m60/](https://www.nvidia.com/en-us/data-center/tesla-m60/)
* NVIDIA Tesla M60 datasheet: [https://images.nvidia.com/content/pdf/tesla/184457-Tesla-M60-datasheet.pdf](https://images.nvidia.com/content/pdf/tesla/184457-Tesla-M60-datasheet.pdf)
