---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Training Progress on MI300X
translated: false
type: note
---

Here's the full status:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GPT-2 760M Training — MI300X (amd-cloud)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current:    iter 16,300 / 445,000  (3.66%)
Tokens:     ~534M / 14.58B tokens processed
Wall time:  ~2h 23m elapsed
Loss:       train 3.41–3.52  |  val 3.4170 (step 16000)
MFU:        108–113% ← excellent
Per-iter:   ~453ms steady state

Loss trend (val):
  13000 → 3.4759
  14000 → 3.4550  ↓
  15000 → 3.4309  ↓
  16000 → 3.4170  ↓  (healthy, still dropping)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Time Remaining Estimate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remaining:    428,700 iters
Compute:      428,700 × 453ms = 194,201s
Checkpoints:  ~429 saves × 63.7s = 27,071s
Total:        ~221,272s ≈ 61.5 hours ≈ 2.56 days

Cost remaining:  ~$123 @ $2/hr
Total cost end:  ~$128

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Summary: Training is running well. Val loss is steadily decreasing, MFU is 108–113% which is excellent for MI300X. At current pace, about 2.56 days remaining (~$123 more).

The checkpoint save every 1000 steps adds ~63.7s overhead (you can see it in the `time 63699ms` entries). That's about 7.5 hours of total overhead across the whole run — not bad.

Your training is healthy. The loss is still going down smoothly. By the numbers:

  Started:  ~07:26 UTC today (Jun 1)
  Finish:   ~late Jun 3 / early Jun 4
  Total:    ~2.7 days wall time
  Cost:     ~$128 total
