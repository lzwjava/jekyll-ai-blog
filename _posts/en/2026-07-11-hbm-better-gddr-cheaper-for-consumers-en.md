---
audio: false
generated: true
image: false
lang: en
layout: post
title: HBM Better GDDR Cheaper for Consumers
translated: false
type: note
---

Question: Why did NVIDIA move back from HBM2 to GDDR6/GDDR6X in consumer GPUs if HBM2 is better?

Answer:

The short answer: **HBM is better technically, but GDDR is much cheaper and easier to scale for consumer GPUs.**

NVIDIA did not "downgrade" from HBM2 to GDDR6X. They split the market:

```
Data Center:
V100 -> A100 -> H100 -> H200
        HBM2 -> HBM2e -> HBM3/HBM3e

Consumer:
GTX/RTX Pascal -> Turing -> Ampere -> Ada
                GDDR5 -> GDDR6 -> GDDR6X
```

Different optimization targets.

## 1. HBM is expensive

HBM requires:

```
GPU die
  |
silicon interposer
  |
HBM stacks
```

Example:

```
        HBM
       ||||||
    ===========
    Interposer
    ===========
       GPU
```

The GPU and memory become one advanced package.

Problems:

* expensive packaging
* lower manufacturing yield
* limited suppliers
* difficult PCB design

For a $599 RTX card, adding HBM could destroy the economics.

GDDR:

```
GPU ---- PCB ---- GDDR chip
GPU ---- PCB ---- GDDR chip
GPU ---- PCB ---- GDDR chip
```

Much cheaper.

---

## 2. Consumer workloads don't need extreme bandwidth as much

A V100:

```
32GB HBM2
900 GB/s
```

is designed for:

```
matrix multiply
large batch training
scientific computing
```

A gaming GPU:

```
RTX 4070:
12GB GDDR6X
504 GB/s
```

also has:

```
huge L2 cache
compression
rendering optimizations
```

Games do not continuously stream giant tensors like training does.

---

## 3. NVIDIA still uses HBM where it matters

Look at H100:

```
H100 SXM:
80GB HBM3
3.35 TB/s bandwidth
```

Because AI training:

```
Transformer:

Attention:
Q @ K^T

MLP:
X @ W

```

is basically:

```
large matrix multiplication
+
memory movement
```

Bandwidth is everything.

---

## 4. Why GDDR6X became good enough

Micron's GDDR6X uses PAM4 signaling:

Traditional:

```
0 -> 1
two voltage levels
```

GDDR6X:

```
00
01
10
11

four voltage levels
```

More bits per clock.

So NVIDIA got:

```
GDDR6:
14-16 Gbps

GDDR6X:
19-24 Gbps
```

without HBM cost.

---

## 5. The interesting AI angle

Your MI50/V100 observation is actually correct:

Old data center cards have a hidden advantage:

```
MI50:
16GB HBM2

V100:
16/32GB HBM2

RTX 4070:
12GB GDDR6X
```

For some AI workloads:

```
VRAM capacity
+
memory bandwidth
```

matter more than gaming-era TFLOPS.

That is why used V100 32GB, MI50, P100, etc. still have a niche.

But the reason NVIDIA doesn't put HBM on RTX cards is simple:

```
RTX customer:
"I want $599 GPU"

AI customer:
"I pay $30,000 for H100"

Different markets.
```

The future is probably a split architecture:

* consumer: GDDR7 + bigger cache
* AI/data center: HBM4/HBM5 + huge memory pools

HBM is not replacing GDDR; they are optimized for different economics.
