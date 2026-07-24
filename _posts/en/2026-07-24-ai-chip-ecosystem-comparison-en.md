---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Chip Ecosystem Comparison
translated: false
type: note
---

**Question: AWS Trainium and Google TPU are behind AMD in AI chips?**

**Answer:**

Short answer: **not exactly.** It depends on which market you mean.

For **general-purpose AI accelerator market (merchant GPU market)**:

```
NVIDIA CUDA ecosystem
        |
        v
AMD Instinct (MI300X / MI325X / MI355X)
        |
        v
Google TPU / AWS Trainium (mostly internal cloud workloads)
```

But this ranking is misleading because TPU and Trainium are **not trying to compete the same way**.

---

## 1. NVIDIA / AMD = sell accelerators broadly

NVIDIA and AMD sell hardware to:

* hyperscalers
* enterprises
* AI labs
* cloud providers
* governments

Example:

```
OpenAI
  |
  +-- NVIDIA H100/H200/B200
  |
  +-- AMD MI300X (some workloads)

Microsoft Azure
  |
  +-- NVIDIA
  +-- AMD
```

The key advantage is ecosystem:

```
CUDA
 |
 +-- PyTorch
 +-- TensorRT
 +-- vLLM
 +-- Triton
 +-- thousands of kernels
```

---

## 2. Google TPU is actually very strong

Google TPU is not "behind AMD" technically.

Google designed TPU because:

```
Google Search
YouTube
Gemini
Bard
Ads
```

need massive internal inference/training.

TPU advantages:

* custom silicon
* optimized for Google's workloads
* huge pod-scale interconnect

Example:

```
1 TPU Pod

thousands of TPU chips
        |
        |
high-speed interconnect
        |
large distributed model
```

Google can avoid NVIDIA margins.

But disadvantage:

```
TPU ecosystem << CUDA ecosystem
```

You cannot simply take a random PyTorch repo and run it.

---

## 3. AWS Trainium is similar

Amazon Web Services Trainium is AWS's custom AI chip.

The strategy:

```
AWS customers
       |
       v
EC2 Trn instances
       |
       v
Trainium chips
```

AWS wants:

* reduce NVIDIA dependency
* lower AI cloud cost
* differentiate AWS

Trainium is especially interesting because AWS already owns:

* networking
* datacenters
* cloud software

The stack:

```
Neuron SDK
   |
   |
Trainium hardware
```

But again:

```
Neuron ecosystem << CUDA ecosystem
```

---

## 4. Revenue comparison is tricky

Your statement:

> AWS Trainium 据说收入几十亿百亿美金

The important distinction:

Trainium **chip revenue ≠ AWS AI infrastructure revenue**.

AWS can make billions from:

```
AI instances
+
storage
+
network
+
managed services
```

even if Trainium chip sales are small.

AWS does not sell Trainium like NVIDIA sells GPUs.

---

## 5. The interesting part: AI software stack

Your earlier point is actually the deeper one.

The future competition is not only chips:

```
Layer 7: AI applications
        |
Layer 6: Agents
        |
Layer 5: Agent frameworks
        |
Layer 4: Model serving
        |
Layer 3: Compiler/runtime
        |
Layer 2: Accelerator
        |
Layer 1: Semiconductor
```

Examples:

```
Claude Code
    |
    v
OpenClaw
    |
    v
Hermes
    |
    v
Pi agent
```

This resembles the Linux ecosystem:

```
Hardware
   |
Kernel
   |
GNU tools
   |
Applications
```

The winner is not necessarily the best chip.

The winner controls the developer ecosystem.

---

## 6. Huawei Ascend comparison

Huawei Ascend is similar:

```
Ascend chip
 |
CANN
 |
MindSpore
 |
AI applications
```

The hard part is not only manufacturing silicon.

It is:

```
developers
+
libraries
+
compiler
+
debugging tools
+
community
```

CUDA took ~15 years to build.

That is why replacing CUDA is extremely hard.

---

My view:

By 2030 the market likely looks like:

```
NVIDIA CUDA ecosystem
        |
        +---- AMD ROCm ecosystem
        |
        +---- Google TPU ecosystem
        |
        +---- AWS Trainium ecosystem
        |
        +---- Huawei Ascend ecosystem
        |
        +---- custom ASICs
```

NVIDIA may lose monopoly, but the AI market is large enough that **multiple trillion-dollar ecosystems can coexist**.

The bigger shift is exactly what you mentioned: AI software stacks (agents, compilers, workflows) are becoming as important as hardware. The "CUDA moat" is real, but AI itself is expanding the battlefield.
