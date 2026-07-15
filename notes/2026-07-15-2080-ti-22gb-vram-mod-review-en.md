---
audio: false
generated: true
image: false
lang: en
layout: post
title: 2080 Ti 22GB VRAM Mod Review
translated: false
type: note
---

Question: How is the RTX 2080 Ti 22GB VRAM mod card? Is it a good AI GPU?

Answer:

This is actually a very interesting "AI poor man's GPU hack". The idea is real, but with important trade-offs.

NVIDIA GeForce RTX 2080 Ti officially has **11GB GDDR6 VRAM**, but the TU102 GPU family has hardware capability beyond that. Modders have demonstrated adding higher-density memory chips and changing BIOS straps to make 2080 Ti cards show **22GB VRAM**. ([Tom's Hardware][1])

Architecture:

```
RTX 2080 Ti
----------------
GPU: TU102
CUDA cores: 4352
Tensor cores: 544
VRAM: 11GB -> 22GB mod
Memory: GDDR6
Bandwidth: ~616 GB/s
FP16 Tensor: ~113 TFLOPS (sparse lower)
PCIe 3.0
```

The 22GB version:

```
RTX 2080 Ti 22GB
----------------
same GPU compute
same memory bandwidth
double capacity
```

Meaning:

* ✅ Can load larger models
* ✅ Can run LLM inference that 11GB cannot
* ✅ Good for experimentation
* ❌ Does not become twice as fast

For AI workloads, VRAM is often the bottleneck.

Example:

RTX 4070:

```
12GB VRAM
Ada architecture
faster compute
```

RTX 2080 Ti 22GB:

```
22GB VRAM
older Turing architecture
slower compute
```

For LLM inference:

```
Qwen 14B FP16

RTX 4070:
OOM

2080 Ti 22GB:
runs
```

So the 2080 Ti wins because it fits.

---

Compared with RTX 3090:

|                  | 2080 Ti 22GB    | RTX 3090  |
| ---------------- | --------------- | --------- |
| VRAM             | 22GB            | 24GB      |
| Architecture     | Turing          | Ampere    |
| CUDA             | 4352            | 10496     |
| Tensor           | 1st gen         | 3rd gen   |
| Memory bandwidth | 616GB/s         | 936GB/s   |
| Training speed   | ~50-60% of 3090 | 100%      |
| Price            | cheap           | expensive |

For **LLM inference**, the gap is smaller.

For **training**, 3090 destroys it.

---

The interesting part is price.

A year ago ¥2500 for a 22GB modded 2080 Ti was reasonable. Today it depends. There are still sellers making these cards, especially in China. ([Reddit][2])

For a personal AI lab:

Good:

```
2080 Ti 22GB
+
cheap AM4/X79 machine
+
Linux
+
vLLM / llama.cpp
```

You get:

* 20B-30B quantized models
* LoRA experiments
* embedding models
* small vision models

Bad:

* full pretraining
* large batch training
* CUDA-heavy research

---

My ranking for your kind of use (local AI experiments):

```
RTX 3090 24GB
    |
    | best balance
    v

RTX 2080 Ti 22GB
    |
    | VRAM/$ king
    v

Tesla P40 24GB
    |
    | cheap but old

MI50 16GB
```

Given you already have RTX 4070 + MI50 experiments, a 2080 Ti 22GB is actually an interesting "VRAM expansion card". It fills the gap:

```
4070:
fast but 12GB

2080 Ti 22GB:
slow but enough memory
```

For an OPL (one person lab) setup, two heterogeneous GPUs are often more valuable than one expensive GPU:

```
RTX 4070
  - fast inference
  - modern CUDA

2080 Ti 22GB
  - large model loading
  - LoRA experiments

MI50
  - ROCm exploration
```

The main risk is not the concept; it is **seller quality**. VRAM rework requires BGA soldering, BIOS testing, thermal validation. Buy only if GPU-Z, stress test, and long CUDA workload screenshots are provided. ([Tom's Hardware][1])

For AI hackers, this card is basically the GPU equivalent of buying used server CPUs: ugly, inefficient, but extremely capable per yuan.

[1]: https://www.tomshardware.com/news/nvidia-geforce-rtx-2080-ti-22gb-mod?utm_source=chatgpt.com "Nvidia's RTX 2080 Ti Can Be Modded to Support 22GB of GDDR6 Memory | Tom's Hardware"
[2]: https://www.reddit.com/r/LocalLLaMA/comments/1ap8h8q/anyone_tried_a_rtx_2080_ti_22gb/?utm_source=chatgpt.com "Anyone Tried a RTX 2080 Ti 22GB?"
