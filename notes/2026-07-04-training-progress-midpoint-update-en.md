---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Midpoint Update
translated: false
type: note
---

**Step 21,119 / 50,000 (42%) — running strong.**

| Metric | Value |
|---|---|
| **Loss** | 1.31 (was 6.0 at step 58, dropped 78%) |
| **LR multiplier** | 0.89 (cosine decay started) |
| **Speed** | ~51,000 tok/sec, ~1.26s/step |
| **Runtime** | 6h 56m elapsed |
| **ETA** | 9h 29m remaining |
| **GPU** | 99%, 11.5GB, 65°C |
| **Data** | epoch 1, pq:15 rg:10 (through 16 of 63 train files) |

Loss trajectory: 6.0 → 1.3. Still dropping — hasn't converged yet. The cosine LR has just started decaying (0.89). It's on track to hit ~0.86 val bpb by step 50k based on the previous run's curve.