---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Dashboard
translated: false
type: note
---

```





---

**Training Summary — Step 44,219 / 50,000 (88.4%)**

| Metric | Value |
|---|---|
| **Progress** | 88.4% — ~5,780 steps to go |
| **Train loss** | ~0.97—1.15 (fluctuating, LR is low at 0.22x) |
| **Speed** | avg ~53,900 tok/s, ~1.21s/step |
| **Runtime** | 14h 33m elapsed |
| **ETA** | ~1h 54m remaining |
| **GPU** | 99% util, 11.5GB VRAM, 65°C |
| **Data** | epoch 1, pq:33 rg:4 (through 33 of 63 train files) |
| **LR multiplier** | 0.22 (cosine decay nearing end) |

Loss is hovering around 1.0 with some fluctuation — typical for the tail end of training when the LR has decayed to 22% and the model is navigating the remaining loss landscape. It should converge around ~0.85—0.90 val bpb by step 50k based on the previous run's curve at similar loss levels.

**ETA: ~2 hours to completion.** Connect with `tmux attach -t train` to watch live.
