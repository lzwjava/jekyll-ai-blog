---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multiple Computers for Specialized Engineers
translated: false
type: note
---

Question: Are there companies that give employees 3–5 computers/laptops for GPU/CPU research or software engineering work?

Answer:

Yes, but it is **not common for normal software engineers**. It usually happens in companies where engineers are doing **hardware, systems, AI, infrastructure, or performance engineering**.

Typical cases:

### 1. GPU / AI hardware companies

Companies like NVIDIA, AMD, and Intel often provide engineers with multiple machines:

Examples:

* Main development laptop
* Linux workstation with high-end GPU
* Dedicated test machine
* Multiple GPU servers through internal clusters

A CUDA kernel engineer, compiler engineer, ROCm engineer, or ML infrastructure engineer may need:

* different GPU generations
* different driver versions
* different CUDA/ROCm versions
* benchmark machines

It is normal to have access to many machines.

---

### 2. AI research labs

Companies like OpenAI, Anthropic, and Google DeepMind usually do not give every researcher 5 laptops, but they provide **huge compute access**:

Typical setup:

```
Engineer desk:
  MacBook Pro / Linux laptop

Remote:
  GPU cluster
    H100
    H200
    TPU
    A100
    MI300X
```

The "multiple computers" are usually servers, not laptops.

---

### 3. CPU / compiler / operating system companies

For example:

* CPU design
* compiler optimization
* kernel development
* virtualization
* database performance

Engineers may have:

```
Laptop
+
x86 workstation
+
ARM machine
+
server machine
+
special hardware board
```

Because they need to test:

```
x86 vs ARM
Linux vs Windows
different CPU generations
different memory architectures
```

---

### 4. Big tech companies

Companies like Google, Microsoft, Meta Platforms, Amazon:

A normal backend engineer:

```
1 laptop
+
cloud access
```

A performance engineer:

```
laptop
+
Linux workstation
+
test servers
+
specialized hardware
```

---

### 5. Startups doing AI infrastructure

This is where it happens more often now.

An AI startup with 20 engineers might have:

```
Engineer:
  MacBook Pro

Office lab:
  4 x RTX 5090 workstation
  8 x H100 server
  AMD MI300X machine
  ARM server
```

Engineers are encouraged to experiment.

---

The interesting part: historically many great engineers did not have expensive hardware.

Examples:

* Linux was created on a cheap PC.
* Early deep learning researchers used tiny GPUs compared with today.
* Karpathy trained early neural networks on consumer GPUs.

But today, for **GPU systems research**, hardware access matters much more.

Your MI50 experiment is actually close to how hardware researchers work:

```
buy old GPU
install driver
read ROCm/CUDA source
benchmark
break things
fix things
repeat
```

A company doing GPU/compiler work might literally have a lab full of old and new cards:

```
GTX 1080
RTX 3090
A100
H100
MI50
MI250
MI300X
```

because compatibility and performance testing require it.

References:

* NVIDIA CUDA documentation: [https://developer.nvidia.com/cuda-zone](https://developer.nvidia.com/cuda-zone)
* AMD ROCm documentation: [https://rocm.docs.amd.com/](https://rocm.docs.amd.com/)
* OpenAI careers: [https://openai.com/careers/](https://openai.com/careers/)
* Anthropic careers: [https://www.anthropic.com/careers](https://www.anthropic.com/careers)
