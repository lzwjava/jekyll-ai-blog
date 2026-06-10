---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flat LR Degradation Results
translated: false
type: note
---

Done. Final results:

```
Step  | v2 (flat LR) | Old (full schedule)
------|-------------|---------------------
130k  | 0.780       | 0.780  (starting checkpoint)
140k  | 0.902       | 0.865
150k  | 0.890       | 0.854
160k  | 0.882       | 0.843
170k  | 0.874       | 0.831
180k  | 0.866       | 0.820
190k  | 0.859       | 0.810
200k  | 0.853       | 0.801
```

min_val_bpb = 0.780 (step 130k). Neither run improved past the starting checkpoint. Both runs degraded — v2 just degraded more (0.853 vs 0.801) due to the momentum mismatch.

The core problem isn't just LR scheduling — it's that extending from 130k to 200k made the model WORSE in both attempts. The model may have already converged at 130k (21.8x tokens:params ratio, near Chinchilla-optimal). Further training is over-training without benefit at this scale.

To actually improve past 0.780, you'd need either:
1. More data (not just more epochs on the same data)
2. Larger model (d16 or d20)
3. Better data quality/filtering

Want me to clean up the checkpoints and keep only the 130k best?
