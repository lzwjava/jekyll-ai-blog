---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: RTX 4070 Training Time Estimate
translated: false
type: note
---

Here’s a practical estimate based on your logs and your hardware (RTX 4070, 12 GB VRAM).

---

## **1. Why your first iteration took 27 seconds**

* The very first iteration is *always* misleadingly slow because:

  * PyTorch `compile=True` triggers *ahead-of-time graph compilation*.
  * Inductor runs autotuning, kernel specialization, graph lowering.
  * CUDA context creation, memory allocations.
  * Dataset first load & pipeline warmup.

A 20–30 second first step is normal.

After warmup, training speed jumps dramatically.

You should **ignore step 0 completely**.

---

## **2. Expected speed after warmup**

Based on your model size (~40M params), block size 1024, batch 16 × grad-accum 32 = **512 sequences/iter**, an RTX 4070 typically achieves:

**~1.5 to 2.5 million tokens/sec MFU is low early but improves**
Real throughput after warmup is typically:

**80–120 ms per iteration**

This is for:

* 40M param model (light)
* fp16 with fused AdamW
* sequence length 1024
* effective batch size 512

---

## **3. You have max_iters = 6000**

So total time is approximately:

**6000 × ~0.1 s = 600 seconds ≈ 10 minutes**

Even if your throughput is slow:

* At **150 ms/iter → 15 minutes**
* At **200 ms/iter → 20 minutes**

This is the right magnitude.

---

## **4. Watch your logs — MFU will normalize**

MFU showing “-100%” is just because the first iteration time is junk.

After 10–20 iterations, you should see:

* MFU ~ 25–40% (normal for 40M model on 4070)
* iter time drop to <200 ms

---

## **5. Summary: How long you must wait**

**About 10–20 minutes total.**
Not hours.

You will know it’s stable once the log shows iteration times around **100–200 ms**.

---

If you want, paste your next ~10 iteration logs and I can calculate exact throughput from your run.
