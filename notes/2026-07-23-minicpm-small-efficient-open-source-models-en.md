---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MiniCPM: Small Efficient Open-Source Models"
translated: false
type: note
---

Question: what's MiniCPM?

Answer:

OpenBMB MiniCPM is a family of **small, efficient open-source foundation models** developed by OpenBMB (with contributions from ModelBest, THUNLP, and RUC Gaoling School of Artificial Intelligence). The main idea is:

> **Make LLMs small enough to run locally/on edge devices while keeping capability close to much larger models.** ([GitHub][1])

Think of it as the Chinese AI ecosystem's answer to models like Microsoft Phi, Meta Platforms Llama small models, and Alibaba Group Qwen small models.

---

## Model evolution

### MiniCPM (text LLM)

The original MiniCPM focused on **small language models (SLMs)**:

* MiniCPM-1B / 2B class
* Surprisingly strong performance compared with 7B–13B models
* Designed for cheap inference and research experiments

The 2024 paper introduced 1.2B and 2.4B parameter models and showed that careful training strategy can make small models competitive with much larger ones. ([arXiv][2])

Example:

```
Llama2-13B
      |
      v
MiniCPM-2B
```

Not because the architecture is magical, but because:

```
better data
+
better training recipe
+
small efficient architecture
=
higher capability / FLOP
```

---

## MiniCPM-V (vision-language)

This is probably the most famous branch.

Architecture:

```
Image
 |
Vision Encoder
 |
Projector
 |
LLM backbone
 |
Text answer
```

Similar idea to:

* GPT-4V
* Gemini Vision
* Qwen-VL

Use cases:

* OCR
* document understanding
* image QA
* charts/tables
* screenshots

The MiniCPM-V family became popular because it delivered strong vision ability with relatively small parameter counts. ([Hugging Face][3])

---

## MiniCPM-o (omni-modal)

The "o" means **omni**.

It combines:

```
text
+
image
+
audio
+
speech output
```

Example:

```
camera stream
      |
      v
MiniCPM-o
      |
      +--> understands scene
      |
      +--> talks back
```

Recent MiniCPM-o versions target real-time full-duplex interaction:

* listen while speaking
* see live video
* voice conversation

The 4.5 version is a 9B-class multimodal model designed for efficient real-time interaction. ([arXiv][4])

---

## MiniCPM4 / MiniCPM5

These are more about **LLM efficiency engineering**.

MiniCPM4 introduced techniques around:

* sparse attention
* efficient inference
* quantization
* long-context optimization

The goal:

```
cloud-scale capability
        ↓
edge device deployment
```

For example:

```
Server:
H100
1000W

vs

Phone:
5-10W
```

MiniCPM tries to push capability into the second category. ([arXiv][5])

---

## Why MiniCPM is interesting technically

From an engineering perspective, it represents a trend:

### 1. Parameter efficiency

Old thinking:

```
bigger model = smarter
```

New thinking:

```
better training + better architecture
=
smaller model with similar capability
```

Example:

```
70B model
    |
    |
    v

7B distilled model
    |
    |
    v

1B model optimized for edge
```

---

### 2. Local AI

MiniCPM targets:

* phones
* laptops
* robots
* embedded devices

Because inference cost matters:

Memory:

```
FP16:

7B params × 2 bytes
≈ 14GB VRAM

1B params × 2 bytes
≈ 2GB VRAM
```

Quantized:

```
1B INT4

≈ 0.5GB
```

So a phone can run it.

---

### 3. Agent direction

Small models are becoming useful as:

* tool routers
* local assistants
* robot brains
* OCR engines
* personal agents

A future architecture might look like:

```
              Cloud LLM
                  |
        -------------------
        |                 |
    Local MiniCPM     Local tools
        |
     phone/robot
```

---

For your background (training GPT-2 760M, running local models, ROCm/GPU experiments), MiniCPM is especially interesting because it is basically the **"how far can we push a 1B model?" research direction**.

A good experiment:

```bash
# compare capability per VRAM

Qwen3-8B
vs
MiniCPM5-1B
vs
Llama-3.2-1B

same hardware:
RTX 4070 12GB
```

Measure:

```
tokens/sec
VRAM
MMLU
HumanEval
Chinese benchmark
agent tool use
```

This is exactly where the industry is moving: **not only scaling bigger, but scaling intelligence efficiency.** ([GitHub][1])

References:

* [MiniCPM GitHub repository](https://github.com/openbmb/minicpm?utm_source=chatgpt.com)
* [MiniCPM paper: Unveiling the Potential of Small Language Models with Scalable Training Strategies](https://arxiv.org/abs/2404.06395?utm_source=chatgpt.com)
* [MiniCPM4: Ultra-Efficient LLMs on End Devices](https://arxiv.org/abs/2506.07900?utm_source=chatgpt.com)

[1]: https://github.com/openbmb/minicpm?utm_source=chatgpt.com "GitHub - OpenBMB/MiniCPM: MiniCPM5-1B: A SOTA 1B on-device LLM, small yet powerful. · GitHub"
[2]: https://arxiv.org/abs/2404.06395?utm_source=chatgpt.com "MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies"
[3]: https://huggingface.co/openbmb/models?utm_source=chatgpt.com "openbmb (OpenBMB)"
[4]: https://arxiv.org/abs/2604.27393?utm_source=chatgpt.com "MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction"
[5]: https://arxiv.org/abs/2506.07900?utm_source=chatgpt.com "MiniCPM4: Ultra-Efficient LLMs on End Devices"
