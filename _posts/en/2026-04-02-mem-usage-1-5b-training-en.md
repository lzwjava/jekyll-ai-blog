---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Usage for 1.5B Model Training
translated: false
type: note
---

77GB breakdown for 1.5B model:

| Component | Memory |
| ----------- | -------- |
| Weights (bf16) | ~3GB |
| Adam states (2 states × fp32 = m & v) | ~12GB |
| Gradients (fp32) | ~6GB |
| **Activations** (batch=16, seq=1024) | **~56GB** |
| **Total** | **~77GB** |

Activations dominate — that's normal. Each layer's intermediate outputs for every token in every sequence add up fast. 56GB for activations is expected on a 1.5B model with seq=1024 and batch=16.

You could technically fit a **bigger batch** since you have ~66GB headroom, but going larger would increase activations proportionally and you might OOM. The current 77GB is a solid sweet spot for this GPU.
