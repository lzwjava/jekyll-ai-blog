---
audio: false
generated: true
image: false
lang: en
layout: post
title: Master Small Scale, Scale Out
translated: false
type: note
---

Yes, the reasoning is basically right. This is actually a very good engineering learning path for LLM systems: **master the primitive operation at small scale → remove unknowns → scale out**.

A few refinements:

## 1. Distributed training: "one → two → many" is exactly the right mental model

The important thing is not just running `torchrun` once. The goal is to make the whole pipeline deterministic:

```
single GPU
   |
   v
single machine, multi GPU
   |
   v
multi machine, multi GPU
   |
   v
large cluster
```

The concepts are mostly the same:

* process management
* communication backend
* parameter synchronization
* checkpointing
* failure recovery
* data sharding

For example, in PyTorch:

Single GPU:

```python
loss.backward()
optimizer.step()
```

Distributed Data Parallel:

```
GPU0 process
    |
    | gradients all_reduce
    v
GPU1 process
```

Mathematically:

Each worker computes:

[
g_i = \nabla L_i(\theta)
]

Then synchronize:

[
g = \frac{1}{N}\sum_{i=1}^{N}g_i
]

Every GPU updates the same model:

[
\theta_{t+1}=\theta_t-\eta g
]

Once you understand this, moving from 2 GPUs to 2000 GPUs is mostly engineering.

---

## 2. Training 10+ distributed models is actually a good idea

Because the first few experiments will reveal hidden problems:

Example progression:

### Experiment 1

GPT-2 124M

```
2 machines
2 GPUs
DDP
```

Goal:

* NCCL works
* checkpoint works

### Experiment 2

GPT-2 350M

```
4 GPUs
```

Goal:

* memory management

### Experiment 3

Long context model

```
8 GPUs
```

Goal:

* communication bottleneck

### Experiment 4

Larger model

```
FSDP / ZeRO
```

Goal:

* model sharding

After 10 experiments, distributed training becomes muscle memory.

---

## 3. The same applies to SFT

Your point is correct:

> learning something is not enough; proficiency + principles + limitations = understanding

For SFT, the layers are:

### Level 1: Usage

Example:

```bash
python train_sft.py \
 --model Qwen \
 --dataset my_data.json
```

You can run it.

---

### Level 2: Understand the mechanism

SFT is basically supervised learning:

Dataset:

```
instruction:
"Explain CUDA"

answer:
"CUDA is..."
```

Converted:

```
tokens:
[Explain][CUDA][...]
```

Loss:

Usually only answer tokens:

[
L=-\sum_t \log P(y_t|x,y_{<t})
]

The model learns:

[
P(answer|instruction)
]

---

### Level 3: Know limitations

SFT problems:

### 1. Catastrophic forgetting

Too much SFT:

```
general ability ↓
specialized ability ↑
```

---

### 2. Data quality dominates

10k excellent examples:

> often better than

10M noisy examples.

---

### 3. SFT does not create reasoning magically

It mostly teaches:

* style
* format
* knowledge patterns
* behavior alignment

For reasoning, other techniques matter:

* RL
* RLAIF
* process supervision
* synthetic reasoning data

---

## 4. This matches the Karpathy-style approach

Karpathy's philosophy is basically:

> don't just call APIs; rebuild the mechanism until the abstraction disappears.

For LLM engineering:

```
nanoGPT
   ↓
train GPT-2
   ↓
distributed training
   ↓
FSDP
   ↓
large-scale training system
```

The jump from RTX 4070 experiments to multi-node clusters is not a different world. It is the same forward pass + backward pass with more infrastructure.

Your "一生二，二生三，三生万物" analogy fits very well here:

```
single GPU training
        |
        v
DDP
        |
        v
FSDP / ZeRO
        |
        v
Megatron / large clusters
```

The key milestone is not "trained a huge model"; it is:

> "I can make distributed training boring."

When distributed training becomes boring, scaling becomes an engineering problem instead of a research mystery.
