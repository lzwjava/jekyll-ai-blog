---
audio: false
generated: true
image: false
lang: en
layout: post
title: Consumer Motherboards Unsuitable for LLM Training
translated: false
type: note
---

**Question: Consumer motherboards with multiple GPUs are not ideal for LLM training, right?**

**Answer: Yes, generally. A consumer motherboard can run multiple GPUs, but it is usually a poor platform for serious LLM training. The main bottlenecks are PCIe topology, bandwidth, power, cooling, and software scaling.**

### 1. PCIe lanes are the biggest problem

Typical consumer CPUs:

* Intel Core i9
* AMD Ryzen 9

usually have:

```
CPU PCIe lanes:
GPU 1: x16
GPU 2: x4 (chipset)
```

or:

```
GPU 1: PCIe x8
GPU 2: PCIe x8
```

Example:

```
RTX 4090 training setup

GPU0
 |
PCIe x16
 |
CPU

GPU1
 |
PCIe x4
 |
Chipset
 |
CPU
```

The second GPU has much lower bandwidth and shares chipset bandwidth.

For LLM training, this hurts because distributed training constantly does:

```
forward()
backward()
gradient sync
       |
       v
 all_reduce()
       |
       v
 NCCL communication between GPUs
```

Communication becomes the bottleneck.

---

### 2. No NVLink on consumer cards

Data center GPUs:

```
H100
 |
NVLink
 |
900 GB/s+
```

Consumer:

```
RTX 4090
 |
PCIe 4.0 x16
 |
32 GB/s
```

Huge difference.

For example:

8x H100:

```
GPU memory:
640GB

NVLink:
fast communication
```

8x RTX 4090:

```
GPU memory:
192GB

communication:
PCIe bottleneck
```

You can train, but scaling efficiency drops.

---

### 3. Physical problems

Consumer boards are not designed for:

```
GPU GPU GPU GPU
```

Issues:

* GPU thickness (3-4 slots)
* blocked airflow
* motherboard bending
* PSU limitations
* VRM overheating

Example:

```
RTX4090
450W

x4 cards

=1800W GPU only
```

You need:

```
2000W+ PSU
server chassis
blower cards
```

---

### 4. Better platforms

For multi-GPU LLM training:

### Option A: Threadripper Pro

Example:

AMD

CPU:

```
64 cores
128 PCIe lanes
```

Topology:

```
GPU0 PCIe x16
GPU1 PCIe x16
GPU2 PCIe x16
GPU3 PCIe x16
```

Much better.

---

### Option B: EPYC server

AMD

Example:

```
EPYC 9004

128 PCIe lanes
12 memory channels
```

Designed for:

```
8 GPU
+
NVLink/NVSwitch
```

---

### Option C: Single powerful GPU

For personal LLM learning:

Usually:

```
1 x RTX 3090 24GB
1 x RTX 4090 24GB
1 x RTX 6000 Ada 48GB
```

beats a messy multi-GPU consumer setup.

A single GPU avoids:

```
NCCL issues
PCIe bottleneck
distributed debugging
```

---

### For your case

Given you are doing:

* nanoGPT
* GPT-2 training
* ROCm experiments
* distributed training learning

A practical progression:

```
Current:
RTX 4070 12GB
+
MI50 16GB experiment

↓


Step 1:
single 3090 24GB

↓


Step 2:
dual GPU workstation

Threadripper Pro
+
2-4 GPUs

↓


Step 3:
EPYC server
+
8 GPUs
```

For learning distributed training, even a consumer board is useful because you learn:

```
torchrun
DDP
NCCL
checkpoint sharding
FSDP
```

but don't expect linear scaling.

Example:

```
2 x RTX4090

ideal:
2x speed

real consumer motherboard:
1.3-1.6x
```

A proper workstation:

```
2x RTX4090

~1.8x
```

Server platform:

```
4-8 GPUs

much closer to expected scaling
```

So: **consumer motherboard multi-GPU is good for experimenting; bad for building an efficient LLM training machine.**
