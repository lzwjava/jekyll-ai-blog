---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Training Configuration Review
translated: false
type: note
---

Got it. Config looks solid for FineWeb sample-10BT (~10B tokens). A few notes:

**Good:**

- `block_size = 1024` — correct for FineWeb
- `compile = True` — good speedup
- `bias = False` — LLaMA-style, correct
- `weight_decay = 0.1` — standard
- `beta2 = 0.99` — fine

**Watch these:**

- `batch_size = 8` with `gradient_accumulation_steps = 64` → effective batch = 512. Reasonable for 125M model
- `max_iters = 12000` → with block_size 1024 and batch 8, that's ~98M tokens per epoch. For 10B tokens you'd need ~100 iterations to see all data once... wait, actually `max_iters` at 12k with those numbers = ~98B tokens, which is fine since FineWeb is 10B
- `dropout = 0.0` — might overfit on longer runs, but fine for dry runs

**One flag:** `max_iters = 12000` means ~98B tokens processed — 10x the dataset size. You might want `max_iters = 100000` or just let it run until loss plateaus. For a 10B token dataset with this config, 12k iters is quite short.

Overall: **it's a good starting point** but I'd bump `max_iters` up significantly if you want to actually train on the full dataset.
