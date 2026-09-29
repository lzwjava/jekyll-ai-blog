---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Training Progress: Step 116 of 3712"
translated: false
type: note
---

There's no tmux session/window named `a` — here's what I found in your tmux sessions:

**Session 1** is running the nanoGPT training (this is the progress you're looking for):

- **Step:** 116 / 3712 (**3.12%**)
- **Loss:** 4.1218 (down from ~4.41 at step 98 — decreasing nicely ✅)
- **Total time:** 104.45m (~1h 44m)
- **ETA:** 3543.5m (~59 hours remaining)
- **Throughput:** ~17,734 tok/sec
- **MFU (bf16):** ~125% (reported, likely includes some measurement quirk)
- **LR multiplier:** 1.00 (still in warmup/constant phase)
- **Epoch:** 1

**Session 0** is just a network proxy (hysteria2/clash-style) routing traffic — not training.

Summary: training is healthy and progressing — loss is trending down from ~4.4 → ~4.12, and it's ~3% through the run with an ETA of roughly 59 more hours.
