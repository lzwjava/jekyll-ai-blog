---
audio: false
generated: true
image: false
lang: en
layout: post
title: d8 Training Summary and Progress
translated: false
type: note
---

```
d8 TRAINING SUMMARY
===================

Model:
  Architecture: depth=8, dim=512, heads=4, head_dim=128, seq=1024
  Parameters:   125,829,354 (~126M)
  FLOPs/token:  273M (3.8x more than d4)

Training config:
  Steps:        5,000
  Batch size:   4,096 tokens/step
  Total tokens: 20,480,000 (~20M)
  Tracker:      MLflow (http://192.168.1.36:5000)

Progress (first 3 steps):
  Step 0: loss 10.398 | 46 tok/sec | dt 88s
  Step 1: loss 10.397 | 53 tok/sec | dt 77s
  Step 2: loss 10.395 | 61 tok/sec | dt 67s
  Val bpb at step 0: 3.209

Steady-state estimate:
  ~60 tok/sec, ~68s/step
  5000 steps × 68s = 340,000s ≈ 94 hours ≈ 4 days

Comparison with d4:
  d4:  37M params, 115 tok/sec, 18s/step
  d8: 126M params,  60 tok/sec, 68s/step
  Speed ratio: 115/60 = 1.9x (expected 3.8x from FLOPs, but torch.compile
  amortizes overhead better on larger models)

Sessions running:
  1.36: tmux dist-master (training) + tmux mlflow (UI on port 5000)
  1.47: tmux dist-worker

MLflow UI: http://192.168.1.36:5000
```
