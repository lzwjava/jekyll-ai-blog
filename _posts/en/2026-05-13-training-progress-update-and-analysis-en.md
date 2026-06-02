---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Update and Analysis
translated: false
type: note
---

## tmux 7 progress — fineweb-gpt3 training

**Currently at iter ~7020 / 19073** (~37% through the 10B-token run).

### Loss curve (val loss every 500 iters)

| step | train | val      |
| ---- | ----- | -------- |
| 4500 | 3.34  | 3.30     |
| 5000 | 3.31  | 3.26     |
| 5500 | 3.27  | 3.26     |
| 6000 | 3.23  | 3.25     |
| 6500 | 3.26  | **3.17** |
| 7000 | 3.22  | 3.18     |

Healthy downward trend. Val is tracking train, no overfitting signal. The dip from 3.25 → 3.17 between step 6000 and 6500 is the biggest single jump in a while — model is still learning useful structure, not plateaued yet.

### Throughput
- **~11.11 s/iter** steady-state, **MFU ~12.86%** at peak each eval cycle
- Eval steps (every 500) take ~29 s — the 18 s extra is eval + checkpoint save
- At 11.11 s/iter, remaining ~12,053 iters → **~37 hours** to reach `max_iters=19073`

### Findings / observations
1. **Training is stable.** No loss spikes, no NaN, no thermal throttle visible. GPU at 66C / 207W from your earlier `nvidia-smi`.
2. **MFU resets each eval window** (drops to ~12.07% right after eval, climbs back to 12.86%). This is just the moving-average warm-up — not a real regression.
3. **~7.5 GB / 12 GB used** — confirms your earlier memory analysis. The `batch_size=4 → 6` headroom is still on the table, but **you shouldn't change it mid-run** since it would invalidate the LR schedule's relationship to optimizer steps. Save that for the next run.
4. **Checkpoints are being saved every 500 iters** (`always_save_checkpoint=True`). That's ~14 checkpoint writes so far — make sure `out-fineweb-gpt3/` isn't filling disk if you only keep one file (nanoGPT overwrites `ckpt.pt`, so should be fine).
5. **Loss at this point**: ~3.18 val is reasonable for a 124M model ~37% through a 10B-token run on FineWeb-Edu. GPT-2 124M on OpenWebText typically lands around 2.85–2.90 val by end of full training, so you've got room to keep dropping.

### TL;DR
Run is healthy, ~37% done, loss curve looks normal, ~37 h remaining at current pace. Nothing to intervene on.
