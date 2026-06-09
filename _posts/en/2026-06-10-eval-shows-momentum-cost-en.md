---
audio: false
generated: true
image: false
lang: en
layout: post
title: Eval Shows Momentum Cost
translated: false
type: note
---

Step 160k eval is in. Summary:

```
Step  | v2 val_bpb | Old val_bpb | v2 smooth_loss
------|-----------|-------------|---------------
130k  | 0.780*    | 0.780       | 2.602
140k  | 0.902     | 0.865       | 2.888
150k  | 0.890     | (no data)   | 2.841
160k  | 0.882     | 0.843       | 2.899
```

*original checkpoint

v2 improving: 0.902 → 0.890 → 0.882 (↓0.010/10k steps)
But still 0.039 worse than old run at same step (0.882 vs 0.843).

At this rate, v2 reaches ~0.850 at step 200k (old run got 0.801). The momentum penalty costs about 3k steps of recovery. Not catastrophic but not great either.

The model IS learning — just slower due to the momentum mismatch. Let it continue, or kill and restart with `--warmdown-ratio=0.33` if you want clean results.
