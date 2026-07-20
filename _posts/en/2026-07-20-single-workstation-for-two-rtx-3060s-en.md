---
audio: false
generated: true
image: false
lang: en
layout: post
title: Single Workstation for Two RTX 3060s
translated: false
type: note
---

Question: For two RTX 3060 GPUs, is it better to build one MSI ATX motherboard with NVLink, or two separate workstations with one GPU each?

Answer:

Short answer: **do not build around NVLink for RTX 3060.** For AI workloads, two RTX 3060 cards in **one workstation** is usually better than two separate machines, but you should treat them as **two independent GPUs**, not one combined GPU.

First, an important correction:

**RTX 3060 does not support NVLink.**

NVLink was available on some higher-end consumer cards:

* RTX 3090 / 3090 Ti → NVLink
* RTX 2080 Ti → NVLink
* RTX Titan → NVLink

RTX 3060 / 3060 Ti / 3070 / 3080 → **no NVLink connector**

The small connector on some GPUs disappeared after Ampere mid-range cards.

---

## Option A: One ATX workstation, 2× RTX 3060

Example:

```
i9-13900KF
MSI Z790 ATX
64GB DDR5
RTX 3060 12GB
RTX 3060 12GB
```

Architecture:

```
             CPU
              |
        PCIe Root Complex
          /          \
     GPU0            GPU1
   12GB VRAM       12GB VRAM
```

Advantages:

### 1. Easier multi-GPU training

PyTorch:

```python
torchrun \
 --nproc_per_node=2 \
 train.py
```

Each GPU gets its own process:

```
process 0 -> cuda:0
process 1 -> cuda:1
```

Data parallel:

```
batch
 |
 +---- GPU0
 |
 +---- GPU1

gradient sync
```

Works with:

* PyTorch DistributedDataParallel
* DeepSpeed ZeRO
* FSDP
* Accelerate

---

### 2. Shared storage

You avoid:

```
machine A
   |
   network
   |
machine B
```

Instead:

```
NVMe SSD
 |
CPU
 |
GPU0/GPU1
```

Much faster for dataset loading.

---

### 3. Lower cost

One:

* motherboard
* CPU
* RAM
* PSU
* SSD

instead of two complete machines.

---

Disadvantages:

### PCIe bandwidth

Many consumer boards:

```
GPU0:
PCIe x16

GPU1:
PCIe x4/x8
```

For RTX 3060:

PCIe x8 is usually fine.

AI training bottleneck is usually:

```
GPU compute
VRAM
memory bandwidth
```

not PCIe.

---

## Option B: Two independent workstations

Example:

```
Machine A:
CPU
32GB RAM
RTX 3060

Machine B:
CPU
32GB RAM
RTX 3060
```

Connect:

```
Machine A
 |
Ethernet
 |
Machine B
```

Advantages:

### 1. More flexible

You can:

* run different experiments
* train different models
* serve different agents

Example:

```
GPU0:
Qwen inference

GPU1:
LoRA training
```

---

### 2. Fault isolation

One machine dies:

```
Machine A down

Machine B continues
```

---

Disadvantages:

### Distributed training becomes harder

You need:

```
NCCL
+
network
+
SSH
+
distributed launcher
```

Example:

```
GPU0
 |
10Gb Ethernet
 |
GPU1
```

Ethernet latency is much higher.

Comparison:

| Connection    | Bandwidth  | Latency  |
| ------------- | ---------- | -------- |
| NVLink        | ~100GB/s   | very low |
| PCIe          | ~16-32GB/s | low      |
| 10Gb Ethernet | ~1GB/s     | higher   |
| 1Gb Ethernet  | ~0.1GB/s   | terrible |

---

## For LLM work specifically

Given your use case:

* nanoGPT
* GPT-2 training
* LoRA fine-tuning
* agent experiments
* inference serving

I would choose:

```
One powerful workstation
        |
        +-- RTX 3060 12GB
        |
        +-- RTX 3060 12GB
```

Not two machines.

A good layout:

```
CPU:
Ryzen 7950X / i9-13900K

RAM:
128GB

Storage:
2TB NVMe

GPU:
3060 12GB
3060 12GB

PSU:
850W-1000W
```

---

But if your goal is scaling into a "token factory":

```
10 GPUs
10 agents
many experiments
```

then separate nodes become attractive:

```
Node1:
GPU0

Node2:
GPU1

Node3:
GPU2

...
```

because orchestration matters more than raw bandwidth:

```
Kubernetes
Ray
Slurm
vLLM cluster
```

---

For **2× RTX 3060 today**:

My ranking:

1. ✅ One ATX workstation, 2 GPUs (best)
2. ✅ One server/workstation board with 4+ PCIe slots
3. ⚠️ Two machines (only if you need independent agents/services)
4. ❌ NVLink plan (RTX 3060 cannot do it)

For AI experimentation, two 12GB RTX 3060s are actually a nice cheap "mini H200 cluster": not powerful, but excellent for learning distributed training, DDP, LoRA, inference serving, and agent workloads.
