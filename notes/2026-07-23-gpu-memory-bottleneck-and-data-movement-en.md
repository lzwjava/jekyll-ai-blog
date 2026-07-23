---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Memory Bottleneck and Data Movement
translated: false
type: note
---

**Question: Why is GPU computing fast but often bottlenecked by memory? In matrix multiplication, why move data instead of computing where the data is?**

**Answer:**

Your intuition is mostly correct. Modern AI is often **memory movement limited**, not pure compute limited.

The key idea:

> A GPU can perform math much faster than it can fetch data.

This is called the **memory wall**.

---

## 1. GPU compute vs memory speed

A modern GPU like NVIDIA H100:

* Tensor cores:

  * ~1,000+ TFLOPS FP16/BF16 compute

* HBM memory:

  * ~3 TB/s bandwidth

The ratio is huge.

Example:

A matrix multiplication:

```
C = A × B
```

For each element:

```
C[i,j] = Σ A[i,k] * B[k,j]
```

The GPU wants:

```
load A
load B
multiply
add
repeat
```

The multiply-add is extremely cheap.

The expensive part:

```
HBM → cache → registers → tensor core
```

Moving bytes costs more time than doing FLOPs.

---

## 2. Why not compute directly in memory?

You asked:

> Can we say data is in disk, then compute directly there and write back?

No, because storage hierarchy is too slow.

Computer architecture:

```
Fastest
        CPU/GPU registers
          ~1 ns

        GPU SRAM/cache
          ~10 ns

        HBM
          ~100 ns

        DDR RAM
          ~100 ns

        SSD
          ~100 μs

        HDD
          ~ms

Slowest
```

A GPU tensor core can do trillions of operations per second.

An SSD cannot feed data fast enough.

If you put compute next to SSD:

```
SSD
 |
 compute
 |
 result
```

the compute unit spends almost all time waiting.

---

## 3. Matrix multiplication example

Suppose:

```
A: 10000 × 10000
B: 10000 × 10000
```

FP16:

Each matrix:

```
10000 × 10000 × 2 bytes

= 200 MB
```

Reading:

```
A + B = 400 MB
```

The output:

```
C = 200 MB
```

Total memory traffic:

```
~600 MB
```

But computation:

```
10000³ × 2 operations

= 2 trillion FLOPs
```

A GPU can do this in milliseconds.

The trick:

**Reuse data.**

Load:

```
A block
B block
```

into fast memory:

```
shared memory
      |
      v
tensor core
```

Compute many times before throwing data away.

This is why optimized GEMM kernels use:

* tiling
* shared memory
* register blocking
* cache reuse

---

## 4. The ideal future: processing near memory

Your idea is actually a real research direction:

### Processing-in-memory (PIM)

Instead of:

```
Memory
   |
   | move data
   v
Compute
```

do:

```
Memory + Compute
        |
        v
     result
```

Examples:

* HBM with compute logic
* AI accelerators with SRAM
* Google's TPU architecture
* Cerebras wafer-scale engine

But it is hard because:

### Memory is optimized for storage

DRAM:

```
cheap
dense
large capacity
```

Compute:

```
complex
hot
power hungry
```

Combining them is difficult.

---

## 5. Why AI especially hits memory bottlenecks

Training:

```
forward:

tokens
 ↓
embedding
 ↓
attention
 ↓
MLP
 ↓
output
```

Every layer:

```
read weights
compute
write activations
```

For large models:

Example:

GPT model:

```
parameters = 1T

BF16 weights:

2 TB
```

Even if compute is infinite:

you must move:

```
2 TB
```

through memory.

The bottleneck becomes:

```
memory bandwidth
```

not FLOPs.

---

## 6. Why GPUs have huge memory bandwidth

CPU:

```
DDR5
~100 GB/s
```

GPU:

```
HBM
~3 TB/s
```

Because AI workloads are:

```
matrix multiply
+
massive parallelism
+
high data reuse
```

GPU design:

```
Thousands of small cores
        +
very wide memory bus
        +
HBM
```

---

## The simplest mental model

Think of GPU like a factory:

```
Tensor cores
===========
very fast workers


Memory
===========
warehouse
```

The workers are so fast that:

```
workers waiting for materials
```

is the main problem.

Optimization is not:

> "make workers faster"

It is:

> "keep workers supplied with data"

That is why modern AI hardware competition is moving from:

```
more FLOPS
```

toward:

```
more HBM
more bandwidth
better interconnect
better memory locality
```

Your "compute where the data is" intuition is exactly the direction of future AI hardware: **near-memory computing and reducing data movement.**
