---
audio: false
generated: true
image: false
lang: en
layout: post
title: Session 1 Training Healthy
translated: false
type: note
---

**Session 1 train is healthy** — it just finished a scheduled eval at the step-1000 milestone, which is why the log paused:

- **Progress:** step 999/3712 done (**26.91%**), just printed `Step 01000 | Validation bpb: 0.882241`
- **Loss:** ~2.8–2.9 (smoothed), val bpb 0.882
- **Speed:** 75.2 s/step, ~13.9k tok/s, **bf16 MFU 98.7%**
- **ETA:** ~3420 min (~57 h) remaining; running for ~22 h total
- **Resources:** GPU 98% util (10.9 GB), process in R state, CPU at full core — no stall

The ~10 min silence was the periodic `--eval-every=250` validation pass (42M tokens). Next it writes the step-1000 checkpoint (~5 GB, same as the 250/500/750 ones at `/mnt/data/nanochat-cache/base_checkpoints/d18`), then training lines resume.
