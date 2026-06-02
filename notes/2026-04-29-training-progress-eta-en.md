---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and ETA
translated: false
type: note
---

Here's the analysis of the running training and ETA.

## Run state

- **Process**: `python3 train.py config/train_fineweb.py` in `tmux 1:` (started Wed Apr 29 13:46 HKT)
- **Now**: Apr 29 22:20 HKT → elapsed ≈ 8 h 34 min
- **Last log line**: `iter 3200: loss 3.4117, time 9332ms, mfu 13.57%`
- **Last checkpoint**: `out-fineweb/ckpt.pt` written at 21:35 (the step-3000 save). Size **1,492,570,892 B ≈ 1.39 GiB**, which matches expectation for a 125M GPT-2 saved with optimizer state (model fp32 ≈ 0.5 GB + AdamW m/v ≈ 1.0 GB).

## Config in use (`config/train_fineweb.py`)

|                            |                                                      |
| -------------------------- | ---------------------------------------------------- |
| dataset                    | fineweb                                              |
| model                      | 12L / 12H / 768d, ~123.6M params                     |
| block_size                 | 1024                                                 |
| batch / grad_accum         | 8 × 64 → effective 512 seq → **524,288 tokens/iter** |
| max_iters / lr_decay_iters | 12000                                                |
| warmup                     | 500                                                  |
| lr                         | 3e-4 → 3e-5                                          |
| eval_interval              | 500 (always_save_checkpoint=True)                    |
| compile                    | True                                                 |

So total tokens at completion ≈ 12000 × 524,288 ≈ **6.29 B tokens** (the comment's "~3B" is stale).

## Loss trajectory

```
step    train    val
0       10.997   10.991
500      5.451    5.508
1000     4.379    4.391
1500     4.063    4.010
2000     3.906    3.852
2500     3.813    3.774
3000     3.744    3.691
```

Still dropping ~0.07 per 500 steps and val < train — healthy, no overfitting. Plenty of room: a 125M GPT-2 on FineWeb-scale data should plateau roughly around 3.0–3.1 val.

## When does it end?

- Per-iter time: 9.33 s (normal) + ~20 s eval every 500 iters → effective **~9.37 s/iter**
- Full run: 12000 × 9.37 ≈ 112,400 s ≈ **31.2 h** wall-clock
- Estimated current iter at 22:20: 30,840 / 9.37 ≈ **iter ~3290**
- Remaining: ~8700 iters × 9.37 s ≈ **22.6 h**
- **ETA: Thu Apr 30, ~20:50 HKT** (±30 min depending on eval overhead)

Next checkpoint save is due at step 3500, ≈ iter 3290 + 210 → in ~33 min from now (around 22:53).

## Things worth noting

- MFU is drifting down slightly (15.4 % → 13.6 %); not concerning, just rolling-average artifact after eval steps.
- `gradient_accumulation_steps = 64` with `batch_size = 8` on a single GPU means each iter is 64 micro-batches — that's why 9.3 s/iter feels long but throughput is fine (~56 K tok/s).
- The comment "~3B tokens seen" on the `max_iters` line is wrong; with block 1024 × eff. batch 512 it's ~6.3B at 12K iters. Worth fixing if you care, but doesn't affect the run.

Want me to keep monitoring and ping you at the next checkpoint, or sample from the current ckpt to sanity-check generations?
