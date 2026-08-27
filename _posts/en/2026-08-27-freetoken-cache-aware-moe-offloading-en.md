---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FreeToken: Cache-Aware MoE Offloading"
translated: false
type: note
---

Question: Is the key idea of FreeToken basically **multiple caches + offloading**?

Answer:

Yes, that is the core intuition, but more precisely:

**FreeToken = intelligent multi-level memory management + adaptive offloading for MoE inference.**

It is not just "put some weights into RAM when GPU is full". The important part is **deciding what should live where and when**.

Think like a computer architecture engineer.

---

## Traditional view

A GPU has limited VRAM:

```
GPU VRAM (fast, small)
        |
        |
PCIe
        |
        |
CPU RAM (slow, large)
        |
        |
SSD (very slow, huge)
```

A naive system:

```
Load model
    |
    v
If GPU full:
    offload everything else to CPU
```

Problem:

MoE routing is dynamic.

Example:

```
Token 1:
Router -> Expert 3, Expert 8

Token 2:
Router -> Expert 50, Expert 71

Token 3:
Router -> Expert 3, Expert 8
```

If you constantly move:

```
CPU RAM -> GPU
GPU -> CPU
```

PCIe becomes the bottleneck.

---

## FreeToken idea

Treat memory like a hierarchy:

```
                 Hot

        GPU VRAM cache
              |
              |
        CPU RAM cache
              |
              |
        SSD storage

                 Cold
```

Similar to CPU caches:

```
CPU

L1 cache  <-- very fast
L2 cache
L3 cache
RAM
SSD
```

The question becomes:

> Which experts deserve the expensive GPU space?

---

## Example

Suppose a 400B MoE model:

```
Experts:

E1
E2
E3
...
E128
```

But for your workload:

```
Most tokens use:

E7   40%
E21  25%
E50  15%

others rarely
```

Then:

GPU:

```
E7
E21
E50
```

CPU:

```
E1-E128 remaining
```

When router asks:

```
Need E7
```

Fast:

```
GPU cache hit
```

When:

```
Need E99
```

Fetch:

```
CPU -> GPU
```

---

## The deeper connection

This is basically **LLM inference as an operating system problem**.

The model is huge:

```
Model = virtual memory space
```

Hardware:

```
VRAM = cache
RAM = memory
SSD = disk
```

The inference engine becomes:

```
             Router

               |
               v

       Memory manager

       /      |       \

    VRAM     RAM     SSD
```

---

## Why this matters for consumer GPUs

Before:

```
Need 80GB GPU
to run 70B+ models
```

After better systems:

```
24GB GPU
+
128GB RAM
+
smart caching

can run much larger models
```

Speed is not datacenter level, but it changes accessibility.

---

For someone building local LLM systems, the important layers are becoming:

```
1. Model architecture
   (Transformer, MoE)

2. Quantization
   (FP16 -> INT8 -> INT4)

3. KV cache optimization

4. Weight cache / expert cache
   (FreeToken style)

5. Kernel optimization
   (FlashAttention, CUDA kernels)

6. Hardware topology
   (PCIe, NVLink, memory bandwidth)
```

FreeToken is mainly attacking **#4: model weight movement and caching**, especially for MoE. It is the same philosophy as CPU cache design: **the fastest memory is the one you avoid accessing.**
