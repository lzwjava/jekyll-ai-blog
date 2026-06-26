---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Pace Reality Check
translated: false
type: note
---

You're absolutely right, I apologize. Here's the REAL picture:

```
REAL TRAINING PACE (from process start time 03:27)
═══════════════════════════════════════════════════
Total elapsed:    8.2 hours (for 41,000 steps)
Real pace:        0.72 s/step (not the displayed 0.070 s/step!)
                  ~12 min per 1000 steps
OVERHEAD:         90% is NOT training — it's eval, checkpoint saves,
                  data loading from parquet shards, Python overhead
═══════════════════════════════════════════════════
Current:          step 41,000 / 47,400  (86.5%)
Val loss:         2.3405 (still declining)
Remaining:        6,400 steps ≈ 76 min ≈ 1.3 hours
Expected finish:  ~13:53 (around 2pm)
```

The displayed "time 702ms" per 10 iters is only measuring the GPU forward+backward pass. The other 90% of wall clock is:

- Eval (100 forward passes every 1000 steps)
- Checkpoint save (1.49GB file write)
- Parquet shard data loading
- Python interpreter overhead

I should have checked the actual process start time instead of trusting the per-iter display. Sorry for the bad estimates earlier.
