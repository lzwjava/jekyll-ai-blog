---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb GPT-2 Training Progress Report
translated: false
type: note
---

## Training status: `out-fineweb-gpt3` (GPT-2 124M on FineWeb-Edu)

**Process**: PID 1200744, `python3.11 -u train.py config/train_fineweb_gpt3.py --compile=False`
**Started**: 2026-05-12 11:49 → **elapsed ≈ 45h 52m**

### Progress

|        | now     | target  | remaining    |
| ------ | ------- | ------- | ------------ |
| iter   | ~14,570 | 19,073  | ~4,500 (24%) |
| tokens | ~7.64 B | ~10.0 B | ~2.36 B      |

Tokens/step = 524,288 (bs 4 × block 1024 × grad_accum 128).

### ETA

- ~11.10 s/iter + ~18 s overhead per 500-iter eval
- 4,500 × 11.10 + 9 × 18 ≈ **13.9 h remaining**
- Wall-clock finish: **~2026-05-14 23:30 HKT** (tonight)

### Loss trajectory (val)

```
step  5000 → 3.260
step 10000 → 3.112
step 12000 → 3.087
step 13000 → 3.035
step 14000 → 3.012   ← best so far
step 14500 → 3.030
```

Val is plateauing in the 3.01–3.06 band; train loss still drifting down (3.04 at 14500). Cosine LR is at ~1.4e-4 (from 6e-4 → min 6e-5), so the last 4.5k iters will see most of the remaining decay.

### Health

- GPU: 100% util, 7.5/12.3 GB, 65 °C, 208 W — fine
- Disk: 664G / 1.8T used — fine
- MFU ~12.86% steady (low because `--compile=False`)
- `always_save_checkpoint=True` → ckpt.pt overwritten every 500 iters (last 09:23, 1.4 GB)

### Notes / decisions worth flagging

- **No "best-only" checkpoint kept** — ckpt at step 14500 (val 3.030) overwrote the better step-14000 (val 3.012). If you care about best val, consider switching to `always_save_checkpoint=False` for the home stretch, or back up `ckpt.pt` after a good eval.
- Comment in config says "bump toward ~190k for full 100B" — you're on the ~10B short run, ending tonight as planned.

Want me to watch for the run finishing, or back up the current ckpt?
