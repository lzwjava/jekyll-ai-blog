---
audio: false
generated: true
image: false
lang: en
layout: post
title: SlowRecovery from
translated: false
type: note
---

Improving. New checkpoint at 150k:

```
Step  | val_bpb  | smooth_loss | Run
------|----------|-------------|--------
130k  | 0.780    | 2.602       | (original, best)
140k  | 0.902    | 2.888       | v2 (spike)
150k  | 0.890    | 2.841       | v2 (recovering)
```

val_bpb: 0.902 → 0.890 (↓ improving)
smooth_loss: 2.888 → 2.841 (↓ improving)
Current raw loss at step 153k: ~2.84 (still trending down)

The model is slowly recovering. Not as fast as the old run (which was at 0.843 by step 160k), but it's moving in the right direction. The momentum mismatch caused a ~12k step penalty but the optimizer is adapting.

Let it run. The next eval at step 160k will be the real test — if val_bpb drops below ~0.85 it's on track. If it plateaus above 0.88, consider killing and restarting with `--warmdown-ratio=0.33`.
