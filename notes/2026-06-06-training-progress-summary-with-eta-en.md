---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Summary with ETA
translated: false
type: note
---

Training is running smoothly. Here's the summary:

  Progress:  step 92,632 / 130,000 (71.26%)
  Loss:      2.78 ~ 2.87 (recent range)
  LR:        0.47
  Throughput: ~55,700 tok/sec (~1.18s/step)
  Elapsed:   1,817 minutes (~30.3 hours)
  ETA:       ~733 minutes (~12.2 hours)
  Epoch:     1 (pq: 19, rg: 7)

Loss has been oscillating in the 2.75-2.87 band over the last ~80 steps — fairly stable, no divergence. Should finish in roughly 12 hours from now if throughput holds steady.
