---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress and ETA Remain Steady
translated: false
type: note
---

Training is still healthy and on schedule.

**Progress**: iter **2480 / 8000** (31%), elapsed 12h 51m, +640 iters since the last check (~3.3h ago).

**Latest val loss**: **3.4900** at step 2250 (3.6912 → 3.6331 → 3.5057 → 3.4900). Still descending but **decay is slowing** — the gap per eval has shrunk from ~0.4 early to ~0.02 now.

**GPU**: 100% util, 211W, 65°C — same throughput, ~18.55s/iter, MFU 13.6%.

**Time remaining**: 5520 iters × 18.55s + checkpoint stalls ≈ **28–29 hours**, ETA roughly **Saturday 2026-05-16, ~05:15 local**.

If val loss flattens further over the next 2–3 evals, you could safely stop early around iter 4000–5000 and save ~15 hours — the final checkpoint will be in `out-gpt2-200m` already. But no need to intervene right now.
