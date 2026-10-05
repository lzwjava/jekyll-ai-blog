---
audio: false
generated: true
image: false
lang: en
layout: post
title: Session 1 Running Smoothly
translated: false
type: note
---

Re-checked session `1` — still running fine, progressing normally:

## Status @ 16:30 (was 14:58)

| Metric | Now | Last check |
| --- | --- | --- |
| Progress | **step 614 / 3712 (16.54%)** | 544 (14.63%) |
| Loss | ~2.97–3.11 (range last 6 steps) | ~2.96 |
| Speed | ~13,000–13,600 tok/s, 77–81 s/step | ~14,000 tok/s, 75 s/step |
| MFU | 91.5–96.5% | ~99.1% |
| ETA | ~3,890 min ≈ **64.8 h ≈ 2.7 days** (finish ~Oct 8) | ~3,955 min |
| GPU | 100% util, 11.32/12.28 GB, 56°C, 158 W | 60°C, 164 W |
| Process | PID 3976056 alive, 13h31m elapsed, 100% CPU | — |

**Checkpoints** (`base_checkpoints/d18/`): step 250 + step 500 saved; next at **step 750** (~2.9 h away, ≈19:25 today).

**One small observation:** throughput has dipped slightly (~13.0–13.6k tok/s, MFU 91–96% vs a steady 14k / 99% earlier), with occasional 80s steps. GPU is still pegged at 100% and temps are fine, so this looks like minor variance (data loading / clocking), not a problem — but worth keeping an eye on. If it keeps sliding, the ETA will stretch a bit.

No errors, no stalls — all good.
