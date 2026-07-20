---
audio: false
generated: true
image: false
lang: en
layout: post
title: Single Workstation for Two 4070 GPUs
translated: false
type: note
---

Question: For two RTX 4070 GPUs, should I use one workstation or two separate machines? Does NVLink matter?

Answer:

For **2× RTX 4070**, the answer is similar but even clearer:

**Use one workstation if your main goal is AI training/inference. Do not expect NVLink — RTX 4070 does not support NVLink.**

RTX 4070:

* Ada Lovelace architecture
* 12GB GDDR6X VRAM
* PCIe 4.0 x16 interface
* No NVLink
* No GPU memory pooling

So:

```
RTX 4070 #1      RTX 4070 #2
12GB VRAM        12GB VRAM

       cannot become

          24GB VRAM
```

They remain two independent 12GB GPUs.

---

## Option A: One high-end workstation (recommended)

Example:

```
CPU: Ryzen 7950X / i9-13900K
RAM: 128GB DDR5
SSD: 2TB+ NVMe

PCIe slot 1:
RTX 4070

PCIe slot 2:
RTX 4070
```

Software view:

```
CUDA:

cuda:0 -> RTX 4070 12GB
cuda:1 -> RTX 4070 12GB
```

PyTorch:

```python
torch.cuda.device_count()

# 2
```

Training:

```
                 model
                   |
        ---------------------
        |                   |
      GPU0                GPU1
      12GB                12GB

        gradient synchronization
```

Good for:

* GPT-2 style training
* LoRA fine-tuning
* DDP experiments
* inference serving
* multiple agents

---

## But there is one important issue: VRAM

Two 4070s do **not** help with a single model that needs >12GB VRAM.

Example:

Qwen 14B:

```
FP16:
14B × 2 bytes ≈ 28GB
```

One 4070:

```
12GB ❌
```

Two 4070:

```
12GB + 12GB

still not simple 24GB ❌
```

You need:

* model parallelism
* DeepSpeed ZeRO
* tensor parallelism

Example:

```
layer 1-20
   GPU0

layer 21-40
   GPU1
```

Possible, but slower.

---

## Option B: Two separate 4070 machines

Example:

```
Machine A

RTX 4070
64GB RAM


Machine B

RTX 4070
64GB RAM
```

Better for:

### Multiple agents

Example:

```
Machine A:
Claude-like coding agent
+ local model inference

Machine B:
training experiments
+ embedding service
```

or:

```
GPU0:
vLLM server

GPU1:
fine tuning
```

---

## Training speed comparison

Single machine:

```
GPU0
 |
PCIe
 |
CPU
 |
PCIe
 |
GPU1

NCCL
```

Usually:

```
fast
```

Two machines:

```
GPU0
 |
10Gb ethernet
 |
GPU1
```

Communication:

```
100x slower than local GPU memory
```

Distributed training suffers.

---

## Motherboard matters

For dual RTX 4070, avoid small mATX boards.

Better:

```
ATX motherboard

slot spacing:

GPU0
|
3-slot gap
|
GPU1
```

Because RTX 4070 cards are usually:

```
2.5-3 slots thick
```

Example:

```
PCIe x16
RTX4070

(empty)

PCIe x16/x8
RTX4070
```

You need airflow.

---

## PSU

Two RTX 4070:

Power:

```
RTX 4070:
~200W each

GPU total:
400W

CPU:
150W

system:
100W

---------------
~650W
```

Recommended:

```
850W Gold PSU
```

---

## My recommendation for your AI experiments

Given your previous GPT-2 / nanoGPT training:

I would choose:

```
Ryzen 7950X
128GB RAM
2TB NVMe

2 × RTX 4070 12GB

850W PSU
ATX board
```

Why?

You get:

```
24GB total GPU compute
46 TFLOPS FP32-ish
2 CUDA devices
excellent DDP learning platform
```

Then later:

```
replace one RTX4070

with RTX3090 24GB
```

and you have:

```
RTX3090 24GB
+
RTX4070 12GB
```

which is actually more useful for LLM work.

For LLMs, **VRAM capacity beats GPU count** most of the time. A used RTX 3090 24GB is often a better AI card than two RTX 4070 12GB cards.
