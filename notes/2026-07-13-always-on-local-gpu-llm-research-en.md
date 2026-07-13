---
audio: false
generated: true
image: false
lang: en
layout: post
title: Always-on local GPU LLM research
translated: false
type: note
---

Question: Given I only have RTX 4070 + possibly AMD MI50, and can build 2-3 cheap GPU machines, what LLM research direction fits my hardware? Is RunPod H200 for 10 hours enough, or should I build always-on machines?

Answer:

Your instinct is correct: **always-on local machines change your research style.**

A rented H200 is good for:

* "I already know what experiment I want"
* run a big benchmark
* train/fine-tune something expensive

But it is bad for:

* daily iteration
* debugging kernels
* modifying architecture
* running experiments overnight
* letting agents (Hermes/Claude Code) inspect logs and source continuously

For research, the loop matters:

```
idea
 ↓
change code
 ↓
train
 ↓
observe
 ↓
debug
 ↓
new idea
```

A local always-on lab improves this loop.

---

## First: do not optimize for "big model training"

With:

* RTX 4070: 12GB VRAM
* MI50: 16GB HBM2 (but older ROCm ecosystem)

You cannot compete on:

```
train 70B model from scratch
```

But you absolutely can research:

```
architecture
optimization
training dynamics
inference
small models
```

This is actually closer to DeepSeek's engineering culture.

---

# Your best research directions with cheap GPUs

## 1. Small MoE research ⭐⭐⭐⭐⭐

This is probably your best fit.

Why?

MoE does not require huge GPUs.

Example:

Dense model:

```
1B parameters
all active
```

MoE:

```
8 experts

total:
4B parameters

active:
1B parameters
```

Your GPU sees only active experts.

You can experiment:

```
RTX4070

train:

GPT-MoE-300M
GPT-MoE-1B
```

Questions:

* How many experts?
* top-1 vs top-2 routing?
* expert collapse?
* load balancing?
* training stability?

This is real research.

---

## 2. Attention / Transformer simplification ⭐⭐⭐⭐⭐

Actually very suitable.

Because you can train small models.

Examples:

Take nanoGPT:

baseline:

```
Attention

O(n²)
```

Modify:

```
FlashAttention
MLA
GQA
Sliding Window Attention
Linear Attention
```

Compare:

```
tokens/sec
memory
loss
quality
```

Your RTX4070 is enough.

---

## 3. Optimizer research ⭐⭐⭐⭐

Your Muon interest fits here.

You can run many experiments.

Example:

Same model:

```
GPT-2 124M

optimizer A:
AdamW

optimizer B:
Muon

optimizer C:
Lion
```

Compare:

```
training loss curve
tokens needed
final quality
```

Cheap GPUs are actually good.

---

## 4. Distillation / small models ⭐⭐⭐⭐

This matches your H200 usage.

Workflow:

Large teacher:

```
H200
Qwen/DeepSeek model
```

Generate:

```
reasoning traces
```

Train:

```
RTX4070
small student model
```

Research:

```
Can 1B model learn 7B behavior?
```

Very realistic.

---

# What about AMD MI50?

Honestly:

For AI research today:

MI50 is interesting mainly because:

* ROCm
* open source stack
* kernel debugging

But not because of raw productivity.

RTX4070:

```
CUDA
FlashAttention
vLLM
Triton
PyTorch
```

works immediately.

MI50:

expect:

```
driver issue
ROCm version issue
kernel compatibility issue
```

However, for you specifically, this pain is valuable.

You like:

```
read source code
debug system
understand stack
```

So keep it.

A good split:

```
RTX4070:
productive experiments

MI50:
ROCm exploration
```

---

# If you build 3 cheap GPU machines

I would not buy random GPUs.

Make a mini cluster:

## Node 1

RTX4070

```
main development
training
```

## Node 2

cheap NVIDIA card

Example:

RTX3060 12GB

```
experiments
agents
inference server
```

## Node 3

MI50

```
ROCm
kernel
compiler
```

Connect:

```
                 Router

                   |
        ----------------------
        |          |          |
     RTX4070    RTX3060     MI50

     train       test       ROCm
```

Run:

* Docker
* Kubernetes (optional)
* Ray
* Slurm (optional)

---

# Your ideal workflow

You + Hermes:

```
Hermes:
read DeepSeek paper

↓

modify nanoGPT

↓

launch experiment

↓

watch logs

↓

analyze result

↓

suggest next experiment
```

This is where local GPUs shine.

---

# About H200 RunPod

Use it strategically.

Not:

"train every day"

Instead:

Monthly:

```
Rent H200 24-48 hours

do:

- teacher generation
- final benchmark
- large experiment
```

Example:

Local:

```
train student model
```

H200:

```
generate 10M reasoning samples
```

Local:

```
distill
```

---

# If I rank your next 12 months:

Given your background:

| Direction             | Hardware fit | Career value |
| --------------------- | ------------ | ------------ |
| MoE                   | ⭐⭐⭐⭐⭐        | ⭐⭐⭐⭐⭐        |
| MLA/KV cache          | ⭐⭐⭐⭐⭐        | ⭐⭐⭐⭐⭐        |
| FlashAttention/Triton | ⭐⭐⭐⭐         | ⭐⭐⭐⭐⭐        |
| Distillation          | ⭐⭐⭐⭐⭐        | ⭐⭐⭐⭐         |
| RLHF/GRPO             | ⭐⭐⭐          | ⭐⭐⭐⭐         |
| Pure RL theory        | ⭐⭐           | ⭐⭐⭐          |
| Training huge models  | ⭐            | ⭐⭐           |

---

My recommendation:

Build your "AI research workstation":

```
RTX4070 + MI50 first
```

Do not buy more GPUs immediately.

Spend 2-3 months making:

```
nanoGPT
   |
   +-- MoE
   |
   +-- MLA
   |
   +-- FlashAttention
   |
   +-- Muon
```

Then you will know exactly which GPU bottleneck matters.

Your advantage is not having H100s. Many people have cloud GPUs.

Your advantage is:

> You can own the whole stack: model → PyTorch → CUDA/ROCm → hardware.

That is a rare profile.
