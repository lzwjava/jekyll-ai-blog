---
audio: false
generated: true
image: false
lang: en
layout: post
title: Real Pace Confirmed
translated: false
type: note
---

Fair skepticism — I was badly wrong before. But this time I'm using the REAL measured pace from checkpoint timestamps, not the misleading per-iter display.

```
REAL MEASUREMENT (checkpoint timestamps):
  Step 46000 (ckpt saved): 12:35:49
  Step 46710 (now):         12:44:20
  Elapsed: 8.5 min for 710 steps
  Real pace: 0.72 s/step (consistent with the 8.2h for 41k steps)

  Remaining: 690 steps × 0.72s = 8.3 min
  Plus eval at step 47000: ~30s
  Total: ~9 min

So yes, ~9 min. The difference from before: I was using the displayed
"702ms per 10 iters" (= 0.07s/step) which is 10x too fast. The real
pace is 0.72s/step. Both measurements now agree.
```

Check back in 10 min and it should be done.
