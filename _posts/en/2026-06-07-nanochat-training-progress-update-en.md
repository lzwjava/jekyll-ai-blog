---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training Progress Update
translated: false
type: note
---

Here's the status:

**Tmux sessions:** Only `0` and `14` exist. Sessions 7 and 12 are gone.

**Nanochat training (tmux 14) — doing great:**

- Step: **144,832 / 200,000** (72.42%)
- Loss: ~2.73-2.76 (healthy, stable)
- Throughput: ~55,700 tok/sec, dt ~1,176ms/step
- Total elapsed: **2,840 minutes** (~47.3 hours)
- ETA: **~1,082 minutes** ≈ **18 hours** remaining
- Learning rate: 0.45
- Epoch 1, pq: 94, rg: 28

So roughly **18 hours left** — should finish sometime tomorrow afternoon/evening. Training looks healthy — loss is stable in the 2.7-2.8 range, no spikes or NaNs.
