---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Run 46% Complete
translated: false
type: note
---

There's no tmux session named `a` — the sessions are `0` (window `mihomo`) and `1` (window `./.venv/bin/python`). Both currently show the same training log. Here's the current progress from the latest step:

**Current status:**

- **Step:** 01708 / 03712 (**46.01%**)
- **Loss:** 2.6921 (recent range ~2.62–2.75)
- **LR multiplier:** 0.84
- **Time per step:** ~58.16s
- **Throughput:** ~18,028 tok/sec
- **BF16 MFU:** 127.60%
- **Epoch:** 1
- **Total time elapsed:** 1646.97 min (~27.4 h)
- **ETA:** 1943.8 min (~32.4 h remaining)

So the run is roughly **46% complete**, with about **32 hours** left. Loss is hovering in the low-2.6 to mid-2.7 range and appears to have roughly plateaued over the last few steps.
