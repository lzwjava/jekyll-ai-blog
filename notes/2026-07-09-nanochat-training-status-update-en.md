---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training Status Update
translated: false
type: note
---

Training is running in **nanochat** on the **codeparrot** dataset. Here's the status:

**Progress:**

- Step 25,601 / 87,000 -- **29.4%**
- Elapsed: 526 min (~8.8h)
- ETA: 1,263 min (~21.1h)
- Remaining: ~61,399 steps

**Loss:**

- Hovering in the **1.22 - 1.47** range, with significant variance step-to-step
- Just hit a lower dip around step 25,534-25,552 (loss ~1.22-1.25), then climbed back to ~1.42
- No clear plateau yet -- still learning, plenty of room to drop

**Performance:**

- ~1.23s/step typical, ~53K tok/s
- bf16_mfu ~162% (clearly a bug in the MFU calc -- numerator/denominator mismatch, probably counting flops wrong for the model config)
- One anomaly at step 25,567: **3.2s dt** when `rg` dropped 1->0 (epoch boundary / data reshuffle event), recovered immediately

**Data pipeline:**

- pq: 15 (prefetch queue depth)
- rg: 0 (recently rolled into a new epoch / reshuffle)
- epoch: 1 (first pass through data)

**At this rate:** ~21h remaining, so total ~30h for 87K steps. Loss is still descending -- no signs of overfitting or convergence yet.
