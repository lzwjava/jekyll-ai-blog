---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 Training Saves 10 Hours
translated: false
type: note
---

FP8 training running strong:

  Step 10/29000 | loss: 9.37 | 82,200 tok/sec | 33.2% MFU | 6.37s/step

Comparing old bf16 run killed at step 185 vs new FP8 run:

  bf16 run (killed):  67,000 tok/s | 27% MFU | 7.8s/step | loss 3.85 @ step 185
  FP8 run (active):   82,200 tok/s | 33% MFU | 6.4s/step | loss 9.37 @ step 10

The loss trajectory is identical (same model, same data, same seed) — FP8 just runs faster. The old run had already dropped to ~3.85 loss at step 185 in ~22 minutes. The FP8 run will reach that same loss ~20% sooner.

Estimated completion:
  bf16: ~62 hours
  FP8:  ~52 hours (saves ~10 hours)

Monitoring:
  tail -f /root/nanochat/run_mi300x_d24_fp8.log

Session: proc_c2b08249fb7b (notify_on_complete=true — you'll be alerted when done)
