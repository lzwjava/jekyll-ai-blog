---
audio: false
generated: true
image: false
lang: en
layout: post
title: Torch Compile Phases and Training Estimates
translated: false
type: note
---

Two phases happening here:

1. **iter 0: 113s** — `torch.compile()` is tracing/optimizing the graph. This is a one-time cost.
2. **iter 50: 21s** — compiled and running

After compilation finishes, you should settle around **1-3 sec/step**. The 164% MFU looks weird — likely a measurement artifact during compile.

**Time estimate:**
- ~100,000 iters remaining
- If ~2 sec/step post-compile → **~56 hours** (~2.3 days)
- If 21 sec/step stays → **~24 days** ← this would be bad

Check `nvidia-smi` right now — is it still 100% GPU-Util? If yes, it's just compile overhead. Once that finishes you'll see a massive speedup.

Also — loss dropping from 11.05 → 7.65 in 50 steps is healthy. Model is learning fine. The question is whether it'll speed up.
