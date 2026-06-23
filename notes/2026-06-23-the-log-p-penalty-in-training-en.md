---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Log P Penalty in Training
translated: false
type: note
---

The key insight the diagram shows:

**log P is the cruelest part.** When your model assigns P = 0.01 to the correct token, log(0.01) = −4.6. When it assigns P = 0.9, log(0.9) = −0.1. The log penalizes low-confidence predictions far more aggressively than a linear scale would — which is exactly what you want when training.

**exp(L) just makes it readable.** Cross-entropy loss L ≈ 1.2 means PPL ≈ 3.3, which you can interpret as "the model is as uncertain as if it had 3 equally likely choices at each step." That's much more intuitive than a raw nats number.

For your GPT-2 760M run on the MI300X — what dataset are you training on and what's your current val PPL landing at?
