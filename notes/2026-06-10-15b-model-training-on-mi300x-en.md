---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1.5B Model Training on MI300X
translated: false
type: note
---

Question: What about training 1.5B parameter models on the same MI300X setup?

Answer:

Training a 1.5B model on your MI300X setup is not only feasible—it’s actually a **much better fit for utilization efficiency**, but there are trade-offs depending on what you optimize for (throughput, MFU, or total training cost).

---

## 1. What changes when you go to 1.5B

Compared to your current ~760M model:

* Parameters: ~2× larger
* Compute per token: ~2× higher
* Memory per step: ~1.6–2× higher (depends on optimizer + activations)
* Attention cost: increases quadratically with sequence length (same seq = same scaling behavior)

---

## 2. What happens to MFU on MI300X

This is the interesting part:

### You will likely see:

* **Higher MFU (%)**
* Often: ~40–55% range (instead of ~37%)

Why?

Because larger models:

* Reduce kernel launch overhead amortization
* Increase arithmetic intensity (FLOPs / byte improves)
* Better saturate MI300X compute units

So paradoxically:

> Bigger model → better MFU efficiency (up to a point)

---

## 3. Throughput vs reality

Even though MFU improves:

* Tokens/sec will drop per step
* But **hardware utilization improves**
* You get more “real compute work per second”

Rough expectation:

* 760M: ~100k tok/s
* 1.5B: ~45k–70k tok/s (depending on batch/seq tuning)

So:

> Lower raw tokens/sec, but better scaling efficiency

---

## 4. Memory considerations (MI300X is key here)

MI300X is actually well-suited:

* 192GB HBM gives you plenty of headroom
* You can likely run:

  * bs=64 @ seq=2048 (still possible)
  * or bs=32 @ seq=4096 more safely

You may even be able to:

* reduce gradient accumulation
* increase per-device batch stability

---

## 5. Training stability improves

Larger models often benefit your current setup:

* FP8 + FA2 becomes more effective
* Gradient noise is reduced (better scaling behavior)
* Less sensitivity to batch fluctuations

---

## 6. The real trade-off

### If your goal is:

#### 🚀 Maximum tokens trained per hour

→ 760M is better (higher tok/sec)

#### 🧠 Better model quality per run

→ 1.5B is significantly better

#### ⚖️ Balanced “research + production”

→ 1.5B is usually the sweet spot on MI300X

---

## 7. Practical recommendation for your setup

Given your current config (~100k tok/s at 760M):

A strong next experiment would be:

* Model: **1.5B**
* seq: 2048 (start here)
* bs: 32 or 64 (test both)
* FP8 + FA2: keep ON
* grad accumulation: adjust to keep global batch stable

Expected result:

* ~1.8–2.2× slower steps
* ~20–40% better MFU efficiency
* noticeably better loss scaling behavior

---

## Bottom line

* ✔ 1.5B is a **better utilization match for MI300X**
* ✔ MFU will likely improve (not worsen)
* ✔ tokens/sec drops, but compute efficiency improves
* ✔ overall training quality/scale benefit is significant

---

If you want, I can help you design the *exact best 1.5B configuration* (batch/seq/accumulation) to push MI300X closer to its real efficiency ceiling (~50%+ MFU territory).
