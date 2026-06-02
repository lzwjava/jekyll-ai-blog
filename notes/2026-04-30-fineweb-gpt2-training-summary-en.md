---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb GPT-2 Training Summary
translated: false
type: note
---

**Status:** Live, healthy, ~72% complete. Started ~2026-04-29 13:46 (tmux session 0).

## Configuration (`config/train_fineweb.py`)

| Param      | Value                                                                               |
| ---------- | ----------------------------------------------------------------------------------- |
| Model      | 12L / 12H / 768 emb, no bias, dropout 0 — **123.59M params**                        |
| Block size | 1024                                                                                |
| Batch      | 8 × 64 grad-accum = effective 512 seq → **524,288 tokens/iter**                     |
| Optimizer  | AdamW fused, lr 3e-4 → 3e-5 cosine, warmup 500, β2=0.99, wd 0.1                     |
| Schedule   | **max_iters = 12,000** (lr_decay_iters = 12,000)                                    |
| Eval       | every 500 iters, 200 batches, checkpoint every eval (`always_save_checkpoint=True`) |
| Compile    | on                                                                                  |
| Dataset    | local `fineweb`                                                                     |

## Throughput

- Steady-state: **~9.34 s/iter** (29 s on iters that follow an eval, due to eval cost)
- MFU: ~13–14% (peaked 15.4% pre-warmup)
- Token budget at completion: **~6.29 B tokens** (12,000 × 524k)

## Loss curve (val every 500 iters)

```
step   train     val
 500   5.4508    5.5082
1000   4.3793    4.3908
2000   3.9059    3.8516
3000   3.7440    3.6908
4000   3.6282    3.5831
5000   3.5656    3.4789
6000   3.5130    3.4665   ← slight plateau
7000   3.4670    3.4154
7500   3.4410    3.3677
8000   3.4243    3.3951   ← small bump
8500   3.4017    3.3534   ← latest
```

- Still descending, but the per-500-iter gain has slowed from ~0.08 in mid-run to ~0.02–0.05 now.
- Val ≤ train throughout (single-batch train vs 200-batch averaged val + dropout=0 — expected).
- No divergence, no NaN, no spikes worth flagging.

## Current state

- **iter 8,600 / 12,000 → ~71.7% done** (~3,400 iters remaining)
- Tokens consumed so far: **~4.51 B**
- Last checkpoint: `out-fineweb/ckpt.pt` — 1.4 GB, written at step 8,500 (2026-04-30 11:54)
- Estimated time to finish: **~8.5–9 hours** (3,400 × 9.34 s + ~7 eval pauses × ~20 s)

## Notes / risk flags

- Config comment says "adjust up to 10000" but `max_iters` is set to 12,000 — run will go the full 12k unless stopped.
- Recent commit `a4c7d87` ("Tune to 10K iters") modifies the 1.5B config, not this file — current run is unaffected.
- Plateau at step 6,000 and bump at step 8,000 are within normal noise; trend is still down.
- `always_save_checkpoint=True` means each eval overwrites `ckpt.pt` with whatever the latest is, regardless of val improvement — fine here since val keeps trending down, but you have no "best" snapshot retained.
