---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FreeToken: MoE Inference Engine"
translated: false
type: note
---

Question: **What is `FlashML-org/FreeToken`?**

Answer: **FreeToken is basically an inference engine for running very large MoE LLMs on hardware that does not have enough VRAM.**

The key idea is:

> **Put the frequently used parts of the model on GPU, keep the huge MoE expert weights in CPU RAM, and stream/cache experts over PCIe only when needed.**

So it is somewhat like **vLLM/SGLang + intelligent CPU/PCIe offloading**, but specifically designed around **large MoE models on consumer/workstation GPUs**. ([GitHub][1])

### The problem it solves

Suppose you have:

```text
290B parameter MoE model

GPU VRAM:       24 / 48 / 96 GB
CPU RAM:        128 / 256 GB
```

You obviously cannot put all 290B weights into VRAM.

But in an MoE model, each token only activates a small number of experts:

```text
                 290B total parameters
                         │
             ┌───────────┴───────────┐
             │                       │
       shared/dense parts       thousands of experts
             │                       │
             ▼                       ▼
           GPU VRAM             CPU RAM
                                  │
                                  │ PCIe
                                  ▼
                                GPU
                         only selected experts
```

FreeToken builds the runtime around this architecture.

Its README explicitly describes it as an **"edge-native Mixture-of-Experts serving engine"** that treats GPU, CPU, host memory and interconnects as one inference platform. ([GitHub][1])

---

## The interesting part: expert offloading

Imagine an MoE layer:

```python
router(x)
    ↓
expert 17
expert 83
expert 421
expert 912
    ↓
weighted sum
```

FreeToken can keep those experts in host RAM:

```text
RAM
┌──────────────────────────────────────────┐
│ Expert 0                                 │
│ Expert 1                                 │
│ Expert 2                                 │
│ ...                                      │
│ Expert 421  ← needed                     │
│ ...                                      │
└──────────────────────────────────────────┘
                  │
               PCIe Gen5
                  │
                  ▼
GPU
┌──────────────────────────────────────────┐
│ currently-needed expert cache            │
│ Expert 421                                │
│ Expert 83                                 │
│ ...                                      │
└──────────────────────────────────────────┘
```

And then it uses **LRU expert caching**, CPU/GPU co-execution and bandwidth-aware scheduling to reduce the cost of moving weights. ([GitHub][1])

This is very relevant to the stuff you've been experimenting with: **GPU VRAM + host RAM + PCIe as one effective memory hierarchy.**

---

## Why this is different from ordinary vLLM

Think of the design space like this:

```text
llama.cpp
    │
    ├── CPU/GPU hybrid
    │
    ▼
vLLM / SGLang
    │
    ├── GPU-centric serving
    │
    ▼
FreeToken
    │
    └── MoE-centric heterogeneous serving
          GPU + CPU + RAM + PCIe
```

FreeToken is particularly interested in situations like:

```text
RTX 4090 / 5090 / RTX 6000 Pro
              +
128–512 GB system RAM
              +
PCIe Gen4/Gen5
              ↓
       giant MoE model
```

rather than requiring:

```text
8 × H100/H200
```

The project currently targets NVIDIA Ampere and newer GPUs with driver 580+ / CUDA 13. ([GitHub][2])

---

## It isn't just an offloader

There are several interesting systems ideas inside it.

### 1. Bandwidth-adaptive execution

FreeToken has a `q*` policy that decides how much work should happen on CPU versus GPU based on the available bandwidth.

Conceptually:

```text
                ┌── GPU compute
MoE expert ─────┤
                └── CPU compute

        choose based on

GPU FLOPS
PCIe bandwidth
CPU memory bandwidth
expert size
batch size
```

This is important because **PCIe can easily become the bottleneck**.

For example:

```text
GPU compute:       enormous
PCIe Gen5 x16:     ~64 GB/s theoretical
CPU RAM:           hundreds of GB/s
```

Sometimes:

```text
load expert → GPU → compute
```

is slower than simply:

```text
compute expert on CPU
```

FreeToken therefore has:

```bash
ft bench bw
```

which measures CPU/PCIe bandwidth and generates a hardware-specific profile used by the runtime. ([GitHub][3])

---

### 2. Double-buffered prefill

During prefill, it can overlap:

```text
GPU computes expert N
        │
        ├───────────────┐
        │               │
        ▼               ▼
     compute        PCIe transfers
                     expert N+1
```

So PCIe transfer isn't necessarily completely serialized with GPU computation.

That's a classic systems optimization:

```text
while GPU computes:
    DMA next expert
```

---

### 3. Dynamic VRAM allocation

This is another interesting feature.

FreeToken can dynamically rebalance VRAM between:

```text
MoE expert cache
        ↕
KV cache
```

without restarting the engine. ([GitHub][1])

So conceptually:

```text
VRAM = 96 GB

┌──────────────────────┐
│ Expert cache  70 GB  │
│ KV cache      26 GB  │
└──────────────────────┘

              ↓ long context

┌──────────────────────┐
│ Expert cache  45 GB  │
│ KV cache      51 GB  │
└──────────────────────┘
```

---

## It also has its own weight format

FreeToken introduces **FTW**, its fast weight format.

You can convert a Hugging Face checkpoint:

```bash
ft checkpoint \
    --model <hf_model> \
    --out <ftw_dir>
```

and then:

```bash
ft serve --model <ftw_dir>
```

The FTW format is designed around fast loading/offloading of MoE experts. ([GitHub][3])

---

## API compatibility is nice

It exposes:

```text
OpenAI API
/v1/chat/completions
/v1/responses

Anthropic API
/v1/messages
```

So existing clients can basically point at:

```text
http://localhost:1919
```

instead of an OpenAI/Anthropic endpoint. ([GitHub][4])

It even has:

```bash
ft launch claude
ft launch codex
ft launch opencode
ft launch openclaw
```

to connect coding agents directly to the local model server. ([GitHub][4])

---

# The hardware angle is probably the most interesting for you

Your previous idea of:

```text
GPU VRAM
   +
system RAM
   +
PCIe
   +
large MoE
```

is basically exactly the problem FreeToken attacks.

For example:

```text
RTX PRO 6000
96 GB VRAM
        +
256 GB DDR5 RAM
        +
PCIe Gen5 x16
        ↓
large NVFP4 MoE
```

Instead of thinking:

> "My GPU has only 96 GB, therefore I can't run a 200–300B model."

FreeToken's philosophy is:

> **VRAM is a cache, not the entire model memory.**

That is a very important conceptual shift.

The README says it targets **290B+ frontier MoE models on consumer hardware**, and supports formats including **MXFP4, NVFP4, FP8 and BF16**. ([GitHub][1])

---

## Current software stack

The implementation is fairly low-level:

```text
Python
  │
  ├── PyTorch 2.11
  ├── Triton 3.6
  ├── FlashInfer
  ├── SGLang kernels
  │
  └── custom C++/CUDA extensions
             │
             ▼
          NVIDIA GPU
```

The repository's build configuration explicitly requires Torch 2.11.x and CUDA 13 tooling, with native C++ extensions for pinned-memory and CPU MoE execution. ([GitHub][5])

---

## Supported models

The project lists models including:

```text
DeepSeek-V4
GLM-5.2
GLM-4.7
Qwen3.8-Flash-Next
Qwen3.6 / Qwen3.5 MoE
Qwen3.8 / Qwen3.6 dense
```

with various FP8/NVFP4/BF16 checkpoints. ([GitHub][6])

---

# In one picture

I'd summarize FreeToken as:

```text
                    FreeToken
                       │
       ┌───────────────┼────────────────┐
       │               │                │
     Model          Scheduler         Memory
       │               │                │
       ▼               ▼                ▼
   giant MoE      bandwidth-aware    VRAM cache
       │             execution          │
       │                                │
       └──────────────┬─────────────────┘
                      │
              PCIe / CPU RAM
                      │
                      ▼
              consumer GPU
```

**It's not a new LLM. It's an LLM inference runtime.**

And technically, I think the most important thing to study in this repo isn't the CLI or API—it is the **MoE expert cache + CPU/GPU execution + PCIe scheduling path**. That's where the interesting systems work is.

[FreeToken GitHub repository](https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com) [FreeToken paper (arXiv)](https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com)

[1]: https://github.com/FlashML-org/FreeToken/blob/main/README.md?utm_source=chatgpt.com "FreeToken/README.md at main · FlashML-org/FreeToken · GitHub"
[2]: https://github.com/FlashML-org/FreeToken/issues/84?utm_source=chatgpt.com "FAQ · Issue #84 · FlashML-org/FreeToken · GitHub"
[3]: https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md?utm_source=chatgpt.com "FreeToken/docs/cli.md at main · FlashML-org/FreeToken · GitHub"
[4]: https://github.com/FlashML-org/FreeToken/blob/main/docs/quickstart.md?ref=explainx&utm_source=chatgpt.com "FreeToken/docs/quickstart.md at main · FlashML-org/FreeToken · GitHub"
[5]: https://github.com/FlashML-org/FreeToken/blob/main/pyproject.toml?utm_source=chatgpt.com "FreeToken/pyproject.toml at main · FlashML-org/FreeToken · GitHub"
[6]: https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com "FreeToken/docs/models.md at main · FlashML-org/FreeToken · GitHub"
