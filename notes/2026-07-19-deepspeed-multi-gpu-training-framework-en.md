---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSpeed Multi-GPU Training Framework
translated: false
type: note
---

Question: What's DeepSpeed? Is it a multi-GPU training framework?

Answer:

Yes. **DeepSpeed is a distributed deep learning training and inference optimization framework from Microsoft**, mainly designed to make **large model training possible on multiple GPUs** (and even thousands of GPUs).

Think of it as a layer on top of **PyTorch Distributed** that solves the problems you hit when scaling from 1 GPU → many GPUs:

* GPU memory limit
* communication overhead
* optimizer state explosion
* checkpoint size
* training throughput

The core idea:

```
PyTorch model
      |
      v
DeepSpeed engine
      |
      +-- ZeRO optimizer
      +-- Distributed Data Parallel
      +-- Memory optimization
      +-- Communication optimization
      +-- Offload CPU/NVMe
      +-- Mixed precision
```

---

## Why DeepSpeed exists: memory explosion

For normal Adam training, a model needs much more memory than just parameters.

Example: FP16 training.

A parameter:

```
weight:              2 bytes (fp16)
gradient:            2 bytes
Adam momentum:       4 bytes (fp32)
Adam variance:       4 bytes (fp32)
master weight:       4 bytes (fp32)

Total ≈ 16 bytes / parameter
```

A 70B parameter model:

```
70B × 16 bytes

= 1.12 TB VRAM
```

Even H100 80GB cannot train it.

DeepSpeed ZeRO splits this.

---

## ZeRO (Zero Redundancy Optimizer)

Normal DistributedDataParallel:

```
GPU0:
 model
 gradients
 optimizer states

GPU1:
 model
 gradients
 optimizer states

GPU2:
 model
 gradients
 optimizer states
```

Every GPU stores everything.

Wasteful.

---

DeepSpeed ZeRO:

### ZeRO Stage 1

Split optimizer states:

```
GPU0:
 optimizer shard A

GPU1:
 optimizer shard B

GPU2:
 optimizer shard C
```

---

### ZeRO Stage 2

Also split gradients:

```
GPU0:
 optimizer A
 gradient A

GPU1:
 optimizer B
 gradient B
```

---

### ZeRO Stage 3

Split parameters too:

```
GPU0:
 parameter shard A

GPU1:
 parameter shard B

GPU2:
 parameter shard C
```

Now a model larger than one GPU can train.

---

Example:

```
70B model

Without ZeRO:

needs ~1TB

With ZeRO-3:

8 GPUs × 80GB

possible
```

---

## DeepSpeed vs PyTorch DDP

Simple DDP:

```python
torchrun \
 --nproc_per_node=8 \
 train.py
```

Each GPU owns full model.

Good for:

* 7B models
* 13B models

---

DeepSpeed:

```bash
deepspeed train.py \
 --deepspeed ds_config.json
```

with:

```json
{
 "zero_optimization": {
   "stage": 3
 }
}
```

Good for:

* 70B+
* trillion parameter experiments

---

## DeepSpeed is not only training

It also has:

### 1. Inference optimization

Example:

A 70B model:

```
FP16:

140GB VRAM
```

DeepSpeed inference can:

* shard weights
* tensor parallel
* optimize kernels

Run on:

```
2 × A100 80GB
```

---

### 2. CPU/NVMe offload

If GPU memory is insufficient:

```
GPU VRAM
   |
   |
CPU RAM
   |
   |
NVMe SSD
```

Example:

Training a 30B model on consumer GPUs.

---

## Compared with other frameworks

| Framework   | Main use                          |
| ----------- | --------------------------------- |
| PyTorch DDP | standard multi-GPU                |
| DeepSpeed   | large model training              |
| FSDP        | PyTorch native equivalent of ZeRO |
| Megatron-LM | huge transformer training         |
| ColossalAI  | similar goal                      |
| Accelerate  | HuggingFace launcher abstraction  |

---

## For your hardware situation

For your RTX 4070 / possible RTX 3090 setups:

### Single RTX 4070 12GB

DeepSpeed does not help much.

You are memory limited but only one GPU.

Better:

* gradient checkpointing
* LoRA
* QLoRA
* smaller batch
* Flash Attention

---

### 2 × RTX 3090 24GB

DeepSpeed starts becoming useful:

```
48GB VRAM total
```

Possible:

* 13B full fine-tuning
* 30B inference
* some larger training with ZeRO

Example:

```
2 x 3090
        |
        v
DeepSpeed ZeRO-2/3
        |
        v
Qwen 14B fine tuning
```

---

### Data parallel vs model parallel

Important distinction:

**DDP:**

```
GPU0: whole model
GPU1: whole model

different data
```

**DeepSpeed ZeRO-3:**

```
GPU0: part of model
GPU1: part of model

same model distributed
```

This is why DeepSpeed matters for LLMs.

---

For your GPT-2 124M/760M training experiments, you probably don't need DeepSpeed. Your RTX 4070 can handle those. DeepSpeed becomes interesting when you move into **7B+ full training or 30B/70B fine-tuning**.
