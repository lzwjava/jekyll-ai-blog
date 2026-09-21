---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Optimizers Start at Different Losses
translated: false
type: note
---

**Question:** Looking at the optimizer comparison plot, why do all optimizers start at different training loss values at epoch 0, rather than all beginning from the same loss?

**Answer:**

Great result! Your experiment successfully ran. Let me explain what's happening.

---

## Why Different Starting Losses?

The key reason is: **the loss reported at "epoch 0" (or the first epoch) is NOT the loss before any training — it is the loss AFTER the first full pass through the dataset.**

During that first epoch, each optimizer is already updating weights **continuously**, and they update weights at **different speeds and directions** from the very first batch. By the time epoch 1 is done, each optimizer has already taken ~235 gradient steps (60,000 samples ÷ 256 batch size), and they've each moved to very different places in parameter space.

---

## Breakdown of Each Optimizer's Behavior

### SGD (orange) — starts highest ~0.48

SGD has **no adaptive learning rate**. In the first epoch, it takes uniform steps in the raw gradient direction. The momentum hasn't built up yet, so it's slow to orient itself. The first few batches are "wasted" finding the right direction → high loss at end of epoch 1.

### AdaGrad (red) — starts ~0.30

AdaGrad accumulates the **sum of all squared gradients** in the denominator. Early on this sum is very small, so the effective learning rate is actually **very large** at the beginning. This causes slightly aggressive steps early, but it stabilizes quickly.

### Adam (blue) — starts ~0.23

Adam uses **bias-corrected** 1st and 2nd moment estimates. Because of the correction term `1/(1 - β₁ᵗ)`, it takes **larger effective steps early on** than it would later. This is the automatic warm-up built into Adam — it gets oriented much faster in epoch 1.

### RMSProp (green) — starts lowest ~0.05

RMSProp is similar to Adam but **without bias correction**. This means in the very first steps, the denominator `√v̂ₜ` is nearly zero (because vₜ is initialized at 0), which makes the effective learning rate **extremely large** in the first few batches. It takes huge steps early — which by chance works well on MNIST but can cause divergence on harder problems. This is exactly the risk the Adam paper warns about.

---

## Visual Summary

```
Epoch 1 loss after ~235 weight updates:

High loss = slow start (SGD)
  SGD       ████████████████████████  0.48
  AdaGrad   ████████████████          0.30
  Adam       ████████████             0.23
  RMSProp   ███                       0.05

Low loss = aggressive early steps (RMSProp)
```

---

## What the Paper Predicted vs What You Got

| Behavior | Paper's Claim | Your Result |
| ---------- | -------------- | ------------- |
| Adam converges fast early | ✅ Yes | ✅ Adam starts at ~0.23, already low |
| SGD is slow initially | ✅ Yes | ✅ SGD starts highest at ~0.48 |
| RMSProp can be unstable without bias correction | ✅ Yes | ✅ RMSProp lucky on MNIST but took huge early steps |
| All converge eventually | ✅ Yes | ✅ All reach ~100% accuracy by epoch 20 |

---

## Why They All Converge to the Same Place

MNIST is a **very easy dataset** — all optimizers eventually saturate at ~100% accuracy because the loss landscape has a very clear, smooth global minimum. On harder datasets (ImageNet, transformers), the differences between Adam and SGD remain significant throughout training — Adam's adaptive learning rate provides a sustained advantage.

---

## Key Takeaway

The different starting losses are **not a bug** — they are the clearest proof that Adam works as described in the paper. Adam's bias-corrected momentum allows it to orient itself faster in the first epoch, which is exactly the "adaptive moment estimation" advantage the paper claims.
