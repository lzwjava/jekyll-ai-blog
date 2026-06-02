---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Training Progress on AMD MI300X
translated: false
type: note
---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GPT-2 760M — MI300X (amd-cloud) — LIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current:    iter 30,800 / 445,000  (6.92%)
Tokens:     ~1.01B / 14.58B tokens
MFU:        108–113% (rock solid)
Per-iter:   ~453ms

Val loss trend:
  13000 → 3.4759
  14000 → 3.4550  ↓
  15000 → 3.4309  ↓
  16000 → 3.4170  ↓
  28000 → 3.2967  ↓
  29000 → 3.2753  ↓
  30000 → 3.2698  ↓  (still dropping steadily)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remaining:  414,200 iters
Est. time:  ~59.4 hours ≈ 2.5 days
Est. cost:  ~$119 remaining
Finish ETA: ~late Jun 3 / early Jun 4 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Training is progressing well. Loss dropped from 3.48 → 3.27 over the last ~17K iters — healthy convergence. MFU holding steady at 108–113%. About 1B tokens processed, 13.6B to go. Roughly 2.5 days left.
