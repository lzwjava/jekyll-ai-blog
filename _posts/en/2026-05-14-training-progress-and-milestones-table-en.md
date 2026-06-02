---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and Milestones Table
translated: false
type: note
---

Training is healthy. Quick status:

|                |                                                                     |
| -------------- | ------------------------------------------------------------------- |
| Process up     | 1:45 elapsed                                                        |
| Params         | 219.4M ✓                                                            |
| Init val loss  | 10.994 (random — expected ~ln(50304) = 10.83)                       |
| GPU            | 100% util, 9.7 GB / 12 GB, 210 W                                    |
| First log seen | `iter 0: loss 11.0089, time 32.4 s` (includes startup eval, normal) |

**Why you don't see iter 1 yet:** `log_interval=20`, so the next print will be at iter 20 (~7 minutes from start).

## When to expect what

| Milestone               | Iter      | ETA from start                   |
| ----------------------- | --------- | -------------------------------- |
| First training log line | 20        | ~7 min                           |
| First real val loss     | 250       | ~1.5 h                           |
| 25% done                | 2,000     | ~12 h                            |
| 50% done                | 4,000     | ~24 h                            |
| 75% done                | 6,000     | ~36 h                            |
| **Run complete**        | **8,000** | **~47 h** (≈ Sat May 16 morning) |

## When to end it

**Don't end early under normal circumstances.** The cosine LR schedule decays from 4e-4 → 4e-5 over all 8,000 iters; cutting short means the last fraction of training never gets the low-LR refinement that locks in final loss.

**Signals it's healthy — let it run:**

- val loss at iter 250 < ~7 (down from 10.99)
- val loss at iter 1000 in the 5–6 range
- val loss monotonically decreasing every checkpoint

**Signals to investigate (not panic-stop):**

- val loss > train loss by a wide margin → data issue
- loss spike or NaN → grad explosion (rare; grad_clip=1.0 should catch it)
- val loss plateaus for 3+ consecutive evals (~750 iters) at any value > 3.5 → optimization stuck

**Reasonable early-stop:**

- If val loss reaches ~2.95 before iter 6000, you *could* stop — you're close to the model's capacity anyway. But the last 25% of training typically buys an extra ~0.05 loss, so I'd still let it finish.

Want me to set up a background watcher that pings you when iter 250 hits (first real signal) and at each subsequent val checkpoint? Or just check in periodically when you ask?
