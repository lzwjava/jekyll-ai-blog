---
audio: false
generated: true
image: false
lang: en
layout: post
title: train/mfu metric incorrectly zero
translated: false
type: note
---

MLflow DB is healthy. Current state:

```
2 runs in the database:
  1. RUNNING  (started Jun 10 ~20:37 UTC)
  2. FINISHED (started Jun 10 ~14:31 UTC)

Latest metrics at step 700:
  train/loss       = 3.707
  train/tok_per_sec = 55,780
  train/mfu        = 0.0        <-- this is wrong, should be non-zero
  train/dt         = 1.175s per step
  total_train_time = 810s (~13.5 min)
```

The DB is live and updating. The RUNNING run is actively logging. What's the issue you're seeing? Is it:

1. The UI can't connect to this DB?
2. The `train/mfu = 0.0` looks wrong?
3. Something else?
