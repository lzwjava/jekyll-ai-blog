---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA Super GPU Refresh Explained
translated: false
type: note
---

Question: What does **"Super"** mean in NVIDIA GPU names?

Answer:

In NVIDIA GPUs, **"Super"** usually means a **refresh / upgraded version of an existing GPU model**, not a completely new architecture.

Example:

* RTX 2060 → RTX 2060 Super
* RTX 2070 → RTX 2070 Super
* RTX 2080 → RTX 2080 Super
* RTX 4070 → RTX 4070 Super

The idea is:

```
same generation
      +
better chip configuration
      +
more CUDA cores / higher clocks / sometimes more memory bandwidth
      =
Super
```

Example comparison:

| GPU            | Architecture | CUDA cores | VRAM        |
| -------------- | ------------ | ---------- | ----------- |
| RTX 4070       | Ada Lovelace | 5888       | 12GB GDDR6X |
| RTX 4070 Super | Ada Lovelace | 7168       | 12GB GDDR6X |
| RTX 4070 Ti    | Ada Lovelace | 7680       | 12GB GDDR6X |

The 4070 Super is basically a stronger 4070 because NVIDIA enabled more of the underlying GPU die.

---

From a semiconductor perspective:

A GPU chip is often produced as:

```
AD104 silicon wafer
        |
        +-- some cores disabled
        |
        +-- RTX 4060 Ti
        |
        +-- more enabled
        |
        +-- RTX 4070
        |
        +-- even more enabled
        |
        +-- RTX 4070 Super / Ti
```

NVIDIA uses different configurations of the same silicon.

---

For AI/LLM workloads, "Super" usually means:

```
more CUDA cores
more Tensor cores
higher FP16/BF16 throughput
similar VRAM
```

Example:

RTX 4070:

```
Tensor cores: 184
FP16 Tensor performance: ~466 TOPS
VRAM: 12GB
```

RTX 4070 Super:

```
Tensor cores: 224
FP16 Tensor performance: ~568 TOPS
VRAM: 12GB
```

So for inference/training:

* matrix multiplication → faster
* attention → faster
* CUDA kernels → faster

but:

**VRAM does not increase.**

For LLMs, VRAM is often the hard limit:

```
Qwen3-8B FP16
≈ 16GB VRAM

RTX 4070 Super 12GB
❌ cannot fit

RTX 3090 24GB
✅ fits
```

So for AI builders, a "Super" card is nice, but moving from:

```
RTX 4070 Super 12GB
        |
        v
RTX 3090 24GB
```

can actually be a bigger upgrade because the memory doubles.

---

NVIDIA naming roughly:

```
GTX 1080 Ti
RTX 2080 Ti
RTX 3080 Ti
RTX 4090

Ti = higher tier

Super = refresh of same tier
```

A simple mental model:

```
xx60       consumer gaming
xx70       strong mainstream
xx80       high end
xx90       workstation / enthusiast

Super      +10~20% improvement
Ti         higher tier
```

For AI work in 2026:

VRAM ranking is often more important:

```
RTX 4090 24GB
RTX 3090 24GB
RTX 5090 32GB
RTX 6000 Ada 48GB
MI300X 192GB
```

A 4070 Super is a fast small-memory GPU; a 3090 is slower per watt but much more useful for local LLM experiments because of the 24GB VRAM.
