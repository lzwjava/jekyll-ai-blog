---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Run Status and Time Estimate
translated: false
type: note
---

Training is running. Here's the status:

```
Step 450 / 445,000  (0.1%)
Loss: 11.1 → 6.35 (decreasing nicely)
Step time: ~450ms (stable, compile warm)
Throughput: ~71,500 tok/s
```

**Time estimate: ~56 hours (~2.3 days)**

```
Remaining steps: 444,550
Step time: 450ms
Remaining time: 444,550 × 0.45 = 199,647 sec = 55.5 hours
```

Earlier 8-10 hour estimate was wrong — that was based on the smoke test (batch=4, no compile). Real step time with batch=32 + compile is ~450ms, not ~81ms.

Current loss trajectory is healthy:
```
step  0: 11.12  (random init)
step 50:  8.61
step 150: 7.22
step 300: 6.62
step 450: 6.35
```

You can leave it running. Check back tomorrow evening — should be around step 200K-250K by then.