---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Training on AMD MI300X
translated: false
type: note
---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GPT-2 760M — MI300X (amd-cloud) — LIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current:    iter 69,550 / 445,000  (15.63%)
Tokens:     ~2.28B / 14.58B tokens
MFU:        108–113% (rock solid)
Per-iter:   ~453ms

Val loss trend:
  13000 → 3.4759
  28000 → 3.2967  ↓
  30000 → 3.2698  ↓
  67000 → 3.1676  ↓
  68000 → 3.1652  ↓
  69000 → 3.1573  ↓  (still dropping steadily)

Train loss:  ~3.19–3.20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remaining:  375,450 iters
Est. time:  ~53.9 hours ≈ 2.25 days
Est. cost:  ~$108 remaining
Finish ETA: ~late Jun 3 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Training is healthy. Loss has dropped from 3.48 (step 13K) to 3.16 (step 69K) — solid convergence. MFU holding at 108–113%. About 2.25 days remaining.