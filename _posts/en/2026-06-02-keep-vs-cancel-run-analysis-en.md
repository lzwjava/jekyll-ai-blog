---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep vs Cancel Run Analysis
translated: false
type: note
---

No, don't cancel. Here's why:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Keep vs Cancel — the math
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sunk cost:    10 hours × $2/hr = $20
Remaining:    ~2.25 days × $2/hr = $108
Total run:    ~$128

If you cancel and restart with bigger batch:
  - You lose $20 + 10 hours of progress
  - MFU is already 108-113% — that's excellent
  - Bigger batch won't meaningfully improve MFU
  - You'd restart from scratch for marginal gain

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The MFU is already 108-113%. That's near-optimal for this hardware. Bumping batch_size from 32 to 64 might save a few percent, but you'd throw away 10 hours of training and $20 to maybe save $5-10 over the whole run. Bad trade.

More importantly:

1. **Loss is dropping nicely** — 3.48 → 3.16, still going down. The model is learning.
2. **You'll get a complete run** — a finished 760M model you can evaluate, sample from, publish. That's the real deliverable.
3. **Pipeline experience** — completing a full training run (start → checkpoint → eval → sample) is worth more than optimizing batch size right now.

The right move is: let this finish, evaluate the model, learn from it. Then your NEXT run can be a bigger model (1.5B, 3B) with optimized settings. That's exactly Karpathy's approach — small experiments first, scale later.

Don't optimize prematurely. Ship this one.
