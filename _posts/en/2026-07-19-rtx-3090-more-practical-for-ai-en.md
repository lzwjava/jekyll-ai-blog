---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3090 More Practical for AI
translated: false
type: note
---

Question: For your AI research direction (Kimi verification, model architecture experiments, MoE, local inference, old GPU clusters), should you buy a second-hand RX 7900 XT or RTX 3090?

Answer:

Given your goals, **RTX 3090 is still the more practical research GPU**, even though ROCm/open-source AMD is attractive.

Your thinking is correct: because H100/A100-class GPUs are expensive, the second-hand market is where individual researchers can play. But for AI experimentation, **software ecosystem matters more than raw hardware**.

Let's compare from your use case.

|                          | RTX 3090 24GB       | RX 7900 XT 20GB  |
| ------------------------ | ------------------- | ---------------- |
| VRAM                     | ✅ 24GB GDDR6X       | 20GB GDDR6       |
| CUDA                     | ✅ Industry standard | ❌ No CUDA        |
| ROCm                     | ❌                   | ✅                |
| PyTorch support          | ⭐⭐⭐⭐⭐               | ⭐⭐⭐              |
| vLLM                     | ⭐⭐⭐⭐⭐               | ⭐⭐               |
| llama.cpp                | ⭐⭐⭐⭐⭐               | ⭐⭐⭐⭐             |
| Training small LLM       | ✅ excellent         | ⚠️ possible      |
| Fine-tuning              | ✅ LoRA/QLoRA        | ⚠️ more friction |
| Multi-GPU experiments    | ✅ mature            | ⚠️ difficult     |
| Used price               | higher              | lower            |
| Research reproducibility | ✅                   | ⚠️               |

---

## Your experiments map better to NVIDIA

Your list:

### 1. Verify Kimi Thinking Machine

You probably want:

* reproduce inference behavior
* run benchmarks
* compare reasoning traces
* test scaling

Most open-source implementations assume:

```bash
pip install torch
pip install transformers
pip install vllm
```

The CUDA path:

```
PyTorch
  |
CUDA
  |
NVIDIA GPU
```

is the default.

With AMD:

```
PyTorch
  |
ROCm
  |
AMD GPU
```

works, but many papers' repos break because:

* CUDA kernels
* FlashAttention versions
* Triton kernels
* custom ops

Example:

```python
import flash_attn
```

works smoothly on NVIDIA.

On AMD, you may spend days fixing build issues.

---

### 2. Transfer frontier lab tricks

This is where NVIDIA wins heavily.

Modern LLM research stack:

```
Transformers
Accelerate
DeepSpeed
FSDP
FlashAttention
Triton
vLLM
SGLang
Megatron
```

Most CI testing happens on NVIDIA.

For example:

```bash
torchrun \
 --nproc_per_node=2 \
 train.py
```

On NVIDIA:

works.

On AMD:

maybe.

---

### 3. MoE experiments

Actually this is very important.

MoE needs:

* memory management
* communication
* expert parallelism

Example:

```
                 router
                   |
        +----------+----------+
        |          |          |
     Expert1    Expert2    Expert3
```

Small MoE:

```
Qwen-MoE style
8 experts
top-2 routing
```

Your RTX 3090:

```
24GB VRAM
```

is very valuable.

RX7900XT:

```
20GB VRAM
```

is already losing 4GB.

For LLMs, VRAM is king.

---

### 4. Local models + old GPU combinations

This is interesting.

You mentioned:

> 探索老旧显卡拼凑方案

Here NVIDIA has a huge advantage.

Examples:

```
3090 24GB
+
3090 24GB

=48GB VRAM
```

With:

```bash
CUDA_VISIBLE_DEVICES=0,1
```

many frameworks understand this.

AMD multi-GPU:

possible, but much less battle-tested.

---

### 5. Attention evolution

Your goal:

```
Transformer
 |
FlashAttention
 |
MQA
 |
GQA
 |
Sliding Window Attention
 |
Linear Attention
 |
RWKV
 |
Mamba
```

You will likely clone many repos.

The probability:

```
Repo works immediately:

RTX3090: 90%

RX7900XT: 50-70%
```

---

## Where RX7900XT is actually interesting

AMD is not a bad choice.

It is interesting if your research goal is:

"Can open-source hardware/software replace CUDA?"

For example:

* ROCm contribution
* kernel optimization
* llama.cpp HIP backend
* GPU programming

Then RX7900XT is fun.

But your current portfolio looks more like:

> AI researcher / model builder

not:

> GPU compiler engineer

---

## Price matters

If:

```
RTX3090:
8000-10000 CNY

RX7900XT:
3000-4000 CNY
```

then the calculation changes.

A 3090 at 10k CNY is bad.

At around:

```
3500-4500 CNY
```

a used RTX3090 is very attractive.

Because:

```
24GB VRAM
+
CUDA ecosystem
+
Tensor cores
+
mature tooling
```

is difficult to replace.

---

## My ranking for you

Given your history:

* trained GPT-2 124M on RTX4070
* interested in nanoGPT
* MoE
* attention research
* local LLM
* reproducing papers

I would rank:

### Option 1 (best)

```
RTX3090 24GB
+
your RTX4070 12GB
```

Use:

* 3090 for training
* 4070 for inference/testing

Very practical.

---

### Option 2

```
2 x RTX3090
```

The "poor man's AI lab":

```
48GB VRAM
```

You can explore:

* 7B fine tuning
* 14B quantized
* MoE prototypes

---

### Option 3

```
RX7900XT
```

Only if:

* price is much lower
* you specifically want ROCm experience

---

My conclusion:

For **your AI portfolio direction**, I would buy:

> **RTX 3090 24GB first.**

ROCm is intellectually attractive, but CUDA is where almost all frontier LLM experiments happen. You can study ROCm later with a cheaper AMD card; your bottleneck today is not FLOPS, it is **VRAM + ecosystem compatibility**.

Your ideal personal AI lab setup:

```
RTX3090 24GB
        |
        +-- nanoGPT
        +-- QLoRA
        +-- MoE toy models
        +-- attention experiments
        +-- vLLM/SGLang

RTX4070 12GB
        |
        +-- inference
        +-- agents
        +-- daily development
```

That is much closer to a small research lab setup.
