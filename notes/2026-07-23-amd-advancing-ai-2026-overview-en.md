---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Advancing AI 2026 Overview
translated: false
type: note
---

Question: What is **AMD Advancing AI 2026**?

Answer:

AMD Advancing AI 2026 is AMD's flagship AI developer/customer conference, similar in role to NVIDIA GTC. It is focused on AMD's push into the AI infrastructure market: GPUs, CPUs, networking, software stack, and AI systems. The 2026 event is held in San Francisco on July 22–23, with CEO Lisa Su giving the keynote. ([AMD][1])

The key idea:

> AMD wants to convince the AI world that there is a serious alternative ecosystem to NVIDIA CUDA + H100/H200/B200.

The stack AMD is promoting:

```
AI Factory
|
+-- Accelerator
|     AMD Instinct MI300X
|     AMD Instinct MI350/MI400 family
|
+-- CPU
|     EPYC server CPUs
|
+-- Networking
|     Pensando / Ethernet fabrics
|
+-- Software
      ROCm
      AI libraries
      PyTorch integration
```

([AMD][2])

## Why this event matters

The AI hardware market today:

```
NVIDIA
  CUDA
  H100/H200/B200
  NVLink
  DGX
       |
       |
       v

AI companies build everything around NVIDIA
```

AMD's strategy:

```
AMD
  ROCm
  Instinct GPUs
  EPYC CPUs
  Open ecosystem
       |
       |
       v

Offer hyperscalers a second source
```

The biggest customers (Microsoft, Meta, OpenAI ecosystem, cloud providers) do not want a single supplier controlling AI compute. AMD is positioning itself as the "second horse". ([Advanced Micro Devices, Inc.][3])

## Things likely discussed

### 1. MI300X / next generation Instinct GPUs

The MI300X is AMD's current serious AI accelerator.

Rough comparison:

| GPU         | Memory      | Main ecosystem |
| ----------- | ----------- | -------------- |
| NVIDIA H100 | 80GB HBM3   | CUDA           |
| AMD MI300X  | 192GB HBM3  | ROCm           |
| NVIDIA H200 | 141GB HBM3E | CUDA           |

AMD's advantage:

* More HBM memory
* Open software philosophy
* Competitive pricing

AMD's weakness:

* ROCm ecosystem is much smaller than CUDA
* Many AI researchers optimize first for NVIDIA

---

### 2. ROCm becoming a CUDA competitor

This is probably the most important part.

CUDA:

```python
import torch

x = torch.randn(1000,1000).cuda()
```

works everywhere because NVIDIA spent 15 years building libraries.

AMD wants:

```python
import torch

x = torch.randn(1000,1000).to("cuda")
```

to also run efficiently on AMD GPUs.

The battle is not only silicon.

It is:

```
Hardware 30%
Software ecosystem 70%
```

---

### 3. AI clusters / "AI factories"

AMD is moving beyond individual GPUs.

The future product is:

```
100,000 GPU cluster

=
GPU
+
CPU
+
network
+
storage
+
compiler
+
software
+
cooling
```

AMD calls this "AI infrastructure". ([AMD][4])

---

## Why it is interesting for you (MI300X / local training perspective)

Given you have experimented with:

* RTX 4070
* MI300X cloud
* GPT-2 training
* nanoGPT
* ROCm

this event is basically about the transition:

```
Old AI:

one researcher
one GPU
CUDA

↓

New AI:

AI factory
1000-100000 accelerators
open hardware/software stack
```

For small developers:

* NVIDIA remains easiest.
* AMD becomes interesting if you operate clusters or need memory capacity.

For example:

A 70B model:

```
FP16:

70B parameters × 2 bytes
≈ 140GB just weights
```

A single RTX 4090/4070 cannot handle it.

MI300X:

```
192GB HBM
```

can potentially run larger models with fewer cards.

---

## My interpretation

AMD Advancing AI 2026 is not mainly about announcing "a faster GPU".

It is AMD saying:

> "AI infrastructure is becoming too important to belong only to NVIDIA."

The real competition:

```
NVIDIA:
CUDA moat + ecosystem + networking

AMD:
hardware + memory + open ecosystem + price

Google:
TPU

Amazon:
Trainium

Microsoft:
Azure AI infrastructure
```

The next 5 years of AI compute will likely be a multi-platform world, not a single NVIDIA-only world. ([AMD][4])

References:

* [AMD Advancing AI 2026 official event page](https://www.amd.com/en/corporate/events/advancing-ai.html?utm_source=chatgpt.com)
* [What to Expect at AMD Advancing AI 2026](https://www.amd.com/en/solutions/data-center/insights/what-to-expect-at-amd-advancing-ai-2026.html?utm_source=chatgpt.com)
* [AMD Announces Advancing AI 2026](https://www.amd.com/en/newsroom/press-releases/2026-4-28-amd-announces-advancing-ai-2026-.html?utm_source=chatgpt.com)

[1]: https://www.amd.com/en/solutions/data-center/insights/what-to-expect-at-amd-advancing-ai-2026.html?utm_source=chatgpt.com "What to Expect at AMD Advancing AI 2026"
[2]: https://www.amd.com/en/newsroom/press-releases/2026-4-28-amd-announces-advancing-ai-2026-.html?utm_source=chatgpt.com "AMD Announces “Advancing AI 2026”"
[3]: https://ir.amd.com/news-events/press-releases/detail/1283/amd-announces-advancing-ai-2026?utm_source=chatgpt.com "AMD Announces “Advancing AI 2026” :: Advanced Micro Devices, Inc. (AMD)"
[4]: https://www.amd.com/en/corporate/events/advancing-ai.html?utm_source=chatgpt.com "AMD Advancing AI 2026 | San Francisco, July 22-23"
