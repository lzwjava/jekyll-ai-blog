---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Loss Progressively Declines
translated: false
type: note
---

Good progress, loss is coming down nicely:

  Progress:  step 107,319 / 130,000 (82.55%)
  Loss:      2.66 ~ 2.71 (recent range)
  LR:        0.30-0.31  (decayed from 0.47)
  Throughput: ~55,700 tok/sec
  Elapsed:   2,105 minutes (~35.1 hours)
  ETA:       ~445 minutes (~7.4 hours)

Since last check (~5 hours ago), training advanced from step 92,632 → 107,319 (~14,700 steps). Loss dropped from 2.78-2.87 → 2.66-2.71 — a nice ~0.1 improvement as LR decayed. Should finish around 7-8 hours from now.
