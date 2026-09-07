---
audio: false
generated: true
image: false
lang: en
layout: post
title: Demand for Deep AI Engineering Skills
translated: false
type: note
---

Question: Will there be strong demand for engineers beyond “LLM application development”—especially pretraining, post-training, CUDA/GPU, and inference infrastructure?

Answer: **Yes. I think this is one of the more important engineering labor markets that will develop over the next 5–10 years.** But I would separate it into layers, because “LLM engineer” will become much more specialized.

### The stack is roughly becoming

```text
                 AI Product / Agents
                        │
              ┌─────────┴─────────┐
              │   LLM Application  │
              │   Agent / RAG      │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │   Post-training   │
              │ SFT / RL / DPO    │
              │ GRPO / RLVR / etc │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │    Pretraining    │
              │ data / tokenizer  │
              │ distributed train │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │   Inference       │
              │ vLLM / kernels    │
              │ quantization      │
              │ KV cache / MoE    │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │ GPU / CUDA        │
              │ CUDA kernels      │
              │ NCCL / PCIe       │
              │ memory / topology │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │ Hardware / Systems│
              │ GPU / HBM / NIC   │
              │ networking        │
              └───────────────────┘
```

And the interesting thing is: **the lower you go, the smaller the talent pool becomes.**

Someone who can do:

```text
PyTorch
   ↓
distributed training
   ↓
CUDA
   ↓
GPU memory
   ↓
NCCL
   ↓
kernel optimization
   ↓
actual hardware behavior
```

is much rarer than someone who can call an LLM API.

### Pretraining engineers

There will be demand for people who understand things like:

```python
loss = cross_entropy(model(tokens), targets)

loss.backward()

# then understand what actually happens:
GPU
 ↓
matmul
 ↓
Tensor Core
 ↓
HBM
 ↓
NCCL
 ↓
another GPU
```

At scale, problems become things like:

* FSDP / ZeRO
* tensor parallelism
* pipeline parallelism
* expert parallelism
* MoE routing
* FP8 / FP4
* checkpointing
* data pipelines
* optimizer memory
* GPU utilization
* communication/computation overlap
* fault tolerance

That's a very different job from "fine-tune a model."

### Post-training will probably grow even faster

As base models become commoditized, companies need to make them **useful for specific objectives**.

For example:

```text
Base model
    ↓
SFT
    ↓
preference optimization
    ↓
RL
    ↓
verifiable rewards
    ↓
tool use
    ↓
reasoning
    ↓
agent behavior
```

So you'll see roles like:

* Post-training engineer
* RL engineer
* RLVR engineer
* reasoning-model engineer
* data/trajectory engineer
* alignment engineer
* evaluation engineer

The interesting part is that post-training increasingly looks like **experimental engineering**:

```text
hypothesis
   ↓
dataset / reward design
   ↓
training run
   ↓
evaluation
   ↓
analyze failure
   ↓
change recipe
   ↓
run again
```

### And CUDA/GPU engineers are particularly valuable

This is probably the part I'd pay attention to in your case.

For example, suppose a model theoretically does:

```text
100 TFLOPS
```

but your actual workload gets:

```text
38 TFLOPS
```

The engineer who can investigate:

```text
Python
 ↓
PyTorch
 ↓
Inductor
 ↓
Triton
 ↓
CUDA kernel
 ↓
SM occupancy
 ↓
register pressure
 ↓
L2
 ↓
HBM
```

is extremely valuable.

Likewise for inference:

```text
request
  ↓
scheduler
  ↓
prefill
  ↓
attention
  ↓
KV cache
  ↓
decode
  ↓
GPU memory
  ↓
PCIe / NVLink
```

A 10–30% improvement at a large inference cluster can be worth enormous money.

---

## The important career distinction

I wouldn't think:

> "I need to become an LLM developer."

I'd think:

> **"I want to become an AI systems engineer who understands the whole stack."**

Something like:

```text
                 LLM
                  │
        ┌─────────┴─────────┐
        │                   │
    Training             Inference
        │                   │
   PyTorch              vLLM
        │                   │
   Distributed           CUDA
        │                   │
     NCCL                GPU
        │                   │
       GPU ─────────────── GPU
```

That skill combination is much harder to commoditize.

And your current interests—**training small models, vLLM/nano-vLLM, KV cache, CUDA, GPU hardware, multi-GPU, memory/PCIe, and eventually kernel optimization**—actually point toward this direction naturally.

You don't need to choose between "LLM" and "CUDA." **The strongest engineers will understand where they meet.**

I can also map out a **2026→2030 AI systems engineer skill tree**—from CUDA basics → Triton → distributed training → pretraining → post-training → inference, with concrete projects at each level.