---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Build 68% Complete
translated: false
type: note
---

Good news — real progress numbers now:

**CUDA stage ~68% complete**

| Item | Count |
|---|---|
| Template instances done | **59 / 120** |
| Non-template `.cu` sources | 69 / 69 ✅ |
| Total CUDA objects | 128 / 189 |

Timeline so far (build started 16:01, now 16:12):
- ~16:09 — compiling `mmq-iq3_s` / `mmq-iq3_xxs` (slow quantized kernels)
- ~16:12 — now compiling `mmf-ncols_10` / `mmf-ncols_11` (flash-attention kernels, generally faster)

**Estimate:** the remaining 61 template instances should take roughly another **15–30 min** (mmq instances are the slow ones and appear to be mostly past). After the CUDA objects finish there's just linking + building the main binaries, which goes relatively quickly.

The original `tail -50` is still alive, so you'll get the final `=== BUILD EXIT DONE ===` and binary listing automatically when it completes. Want me to watch it and check back in ~10 minutes, or check for early signs of errors?
