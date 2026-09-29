---
audio: false
generated: true
image: false
lang: en
layout: post
title: Session 1 Training Running
translated: false
type: note
---

Training is now running. Session 1 has passed compilation and is training.

## Progress (session 1, pane 0)

- **Compile finished** — validation ran: `Step 00000 | Validation bpb: 3.171`
- **Now at step 20 / 3712** (0.54%), loss dropping cleanly: **10.40 → 6.85**
- LR still warming up (`lrm: 0.53`, ramping toward 1.0)

### Throughput
- **~17.9k tok/sec**, **~127% bf16 MFU** (over 100% because it's measured against bf16 peak FLOPS while using FP8/FA3 — this is healthy)
- **~58.4 s/step** (512 grad-accum micro-batches per step)

### ETA
- ~**60 hours** (`eta: 3601m`) for the full 3712 steps.

### Everything looks normal
- Loss curve is behaving as expected (steep early decline).
- No errors, `pq: 0 rg: N` counters incrementing normally.

One thing worth flagging: **~58 s/step is on the slow side**, mostly because each of the 512 micro-batches is tiny (2×1024 tokens) and there's likely a fixed per-micro-batch overhead. If you want, I can investigate whether raising `--device-batch-size` or reducing accumulation overhead could shave time off that ~60h ETA. Want me to dig into the step-time breakdown?