---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mixing NVIDIA and AMD GPUs
translated: false
type: note
---

Question: Can we mix different NVIDIA GPUs (RTX 4070 + RTX 3090), and can we mix NVIDIA + AMD GPUs in one AI workstation?

Answer:

## 1. RTX 4070 + RTX 3090: Yes, totally fine

This is a very common setup for AI hobbyists/researchers.

Example:

```
Machine

CPU
 |
 +-- RTX 3090 24GB  (cuda:0)
 |
 +-- RTX 4070 12GB  (cuda:1)
```

PyTorch sees:

```python
import torch

print(torch.cuda.device_count())

# 2

for i in range(2):
    print(torch.cuda.get_device_name(i))
```

Output:

```
0 NVIDIA GeForce RTX 3090
1 NVIDIA GeForce RTX 4070
```

CUDA does not require identical GPUs.

---

## But there are trade-offs

### Training with DDP

Example:

```
batch
 |
 +----------+
 |          |
3090       4070

24GB       12GB
```

The problem:

The smaller GPU limits the batch size.

If your model needs:

```
GPU0: 20GB
GPU1: 20GB
```

then:

```
3090: OK
4070: OOM
```

The solution:

Use:

* uneven batch allocation
* model parallelism
* ZeRO
* FSDP

or simply:

```
3090 -> training
4070 -> inference / experiments
```

This is often the best practical setup.

---

## For LLM work, RTX3090 + RTX4070 is actually better than 2×4070

Because:

RTX3090:

```
24GB VRAM
384-bit memory bus
936 GB/s bandwidth
```

RTX4070:

```
12GB VRAM
192-bit memory bus
504 GB/s bandwidth
```

For LLM:

VRAM matters a lot.

Example:

A 13B model:

```
FP16:
13B × 2 bytes ≈ 26GB
```

3090:

```
24GB
almost fits with quantization
```

4070:

```
12GB
needs more compression
```

---

# 2. NVIDIA + AMD GPU together?

Example:

```
RTX3090
+
AMD MI50 / Radeon Pro VII
```

Physically:

Yes.

Software:

Much harder.

---

## CUDA world

Most AI frameworks:

```
PyTorch
 |
CUDA
 |
NVIDIA GPU
```

NVIDIA path:

```
PyTorch
 |
CUDA
 |
RTX3090
```

works perfectly.

---

AMD path:

```
PyTorch
 |
ROCm
 |
AMD GPU
```

is a separate ecosystem.

You cannot do:

```
one PyTorch process

cuda:0 RTX3090
+
rocm:0 AMD MI50
```

normally.

They are different backends.

---

## You can run both separately

Example:

```
Machine:

RTX3090
 |
CUDA
 |
vLLM server


AMD MI50
 |
ROCm
 |
PyTorch experiment
```

Linux can handle this.

You just run different processes.

---

## Why NVIDIA + AMD is uncommon

The problem is not hardware.

The problem is software stack.

NVIDIA:

```
CUDA
cuDNN
TensorRT
FlashAttention
xFormers
vLLM
DeepSpeed
```

AMD:

```
ROCm
MIOpen
HIP
```

Many cutting-edge AI libraries optimize NVIDIA first.

---

## Exception: if you like low-level experimentation

For someone like you who likes:

* training GPT-2 from scratch
* nanoGPT
* GPU infrastructure
* ROCm exploration

AMD cards are interesting.

Example:

```
RTX3090:
main LLM work


AMD MI50:
learn ROCm
kernel experiments
cheap compute
```

This is actually a fun lab.

---

## My ranking for an AI workstation

### Best practical

```
RTX3090 24GB
+
RTX4070 12GB
```

⭐⭐⭐⭐⭐

---

### Also good

```
2 × RTX3090
```

⭐⭐⭐⭐⭐

(but power/heat)

---

### OK

```
2 × RTX4070
```

⭐⭐⭐⭐

(good compute, limited VRAM)

---

### Experimental

```
RTX3090
+
AMD MI50
```

⭐⭐⭐

(great learning, less convenient)

---

### Avoid

```
RTX4070
+
AMD consumer GPU
```

unless you specifically want ROCm.

For a small "AI factory" at home, I would build around **one NVIDIA ecosystem first**. Mixing NVIDIA + AMD is more like running a mini research lab.
