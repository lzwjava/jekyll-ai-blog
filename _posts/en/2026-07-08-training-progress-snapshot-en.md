---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Snapshot
translated: false
type: note
---

**Step 182 / 14,500 (1.26%)** — running well:

| Metric | Value |
| -------- | ------- |
| Loss | **3.76** (down from 10.4 at start) |
| LR | 1.00 (peak — warmup complete) |
| Step time | **7.78s** |
| Tok/sec | **134,700** |
| MFU | **65%** |
| Elapsed | **22 min** |
| ETA | **~31 hours** (~Jul 9 12:30 UTC) |

Loss curve looks healthy — dropped from 10.4 → 3.76 in 182 steps. No signs of instability.

To check again later: `ssh root@38.80.152.249 -p 30520` then `tmux attach -t 0` to watch live.
