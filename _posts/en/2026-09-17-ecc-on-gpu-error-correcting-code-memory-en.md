---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ECC on GPU: Error-Correcting Code Memory"
translated: false
type: note
---

Question: What does ECC mean on a GPU card?

Answer: **ECC = Error-Correcting Code** memory.

On a GPU, ECC is a hardware mechanism that detects and, in many cases, corrects **bit errors in VRAM**.

### Why it matters

A GPU stores model weights, activations, gradients, etc. in VRAM. A memory bit can occasionally flip:

```text
Expected:  10110110
Actual:    10110010
                  ^
               bit flipped
```

With ECC memory, the GPU stores additional parity/check bits:

```text
data + ECC bits
   ↓
memory controller
   ↓
detect error
   ↓
correct 1-bit error
```

Typically:

* **Single-bit error** → detected + corrected
* **Some multi-bit errors** → detected, but generally not correctable
* Errors are reported through GPU management tooling

### Why you'd care for ML

For training large models, ECC is particularly useful because jobs can run for **hours/days across many GPUs**. A random VRAM bit flip could otherwise silently corrupt:

```text
weight
  ↓
activation
  ↓
gradient
  ↓
checkpoint
```

and potentially poison the training run.

The tradeoff is that ECC requires extra memory capacity/bandwidth and can have a small performance/capacity cost depending on the GPU architecture.

For example, NVIDIA datacenter GPUs such as **A100/H100** support ECC, while many consumer GeForce cards historically don't expose ECC VRAM.

A useful distinction:

```text
ECC enabled
    ≠
"GPU is more computationally accurate"

ECC protects
    ↓
memory contents
    ↓
against hardware bit errors
```

It does **not** make FP16/BF16/FP32 arithmetic itself error-correcting.

If you're comparing ECC behavior on **MI300X vs H100**, I can break down exactly what ECC protects, how much VRAM is consumed, and how to inspect/monitor ECC errors from CLI.
