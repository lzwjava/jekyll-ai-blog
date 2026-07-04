---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Training Progress and Metrics
translated: false
type: note
---

**SFT running: Step 305 / full epoch (3.4%)**

| Metric | Value |
| --- | --- |
| **Loss** | ~1.7–1.8 (down from 2.4 at step 7) |
| **Speed** | ~50,000 tok/s, ~1.3s/step |
| **Runtime** | 6.4 min elapsed |
| **Progress** | 3.4% of dataset (3.3M tokens seen) |
| **LR** | 1.00 (warmup done, at max) |
| **GPU** | 100%, 8.7GB, 64°C |
| **Epoch** | 1 |

Loss is trending down. The full epoch will cover ~1M conversations, so there's a long way to go. It's saving checkpoints every 500 steps — first eval checkpoint at step 500.

Attach with `tmux attach -t 0`.
