---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Running Normally, 19% Complete
translated: false
type: note
---

There's no tmux session named `a` — I found sessions `0` and `1`, both showing the same training run. Here's the current status:

**Training progress: ~19.4% complete**

| Metric | Value |
|---|---|
| Step | 721 / 3,712 (19.42%) |
| Loss | 3.0204 (bouncing around 2.9–3.05) |
| LR multiplier | 1.00 |
| Step time | ~58.1 s |
| Throughput | 18,049 tok/sec |
| Epoch | 1 |
| Elapsed | ~691 min (11.5 h) |
| ETA | ~2,907 min (~48.4 h remaining) |

**Summary:** Training is running normally and steadily. Loss is fluctuating around ~3.0 with no clear downward trend yet (expected early on, at ~19% through epoch 1). At the current pace, it'll finish in roughly **2 more days**.

Note: `bf16_mfu: 127.76` looks odd (>100%), but that's likely just how the metric is computed (possibly reporting against a reference point rather than theoretical peak).

Want me to keep monitoring, or dig into anything specific (e.g., the training config, why MFU >100%, or the `pq`/`rg` counters)?
