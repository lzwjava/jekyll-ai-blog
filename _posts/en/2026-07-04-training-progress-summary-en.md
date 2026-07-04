---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Summary
translated: false
type: note
---

**Training is running**. Already at step 67/50000:

```
step 00067/50000 | loss: 5.89 → 5.90 | lrm: 1.00
dt: 1195ms/step | tok/sec: 54,834
epoch: 1 | total time: 1.14m | eta: 998m (~16.6h)
```

Loss is dropping from ~6.0 at step 58 to ~5.89 at step 67 — normal initial descent for a freshly initialized model with vocab=32768 (random init loss = log2(32768) ≈ 15).

Training in tmux session **train**. Connect with:
```
tmux attach -t train
```

Check summary any time:
```
bash /mnt/data/zz/train_log.sh --summary
```