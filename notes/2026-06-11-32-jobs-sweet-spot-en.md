---
audio: false
generated: true
image: false
lang: en
layout: post
title: 32 Jobs Sweet Spot
translated: false
type: note
---

Done. Here's the benchmark:

```
Jobs    Time     Speedup
────    ────     ───────
 8      24.1s    1.0x (baseline)
 32      9.9s    2.4x  ← new default
 64      9.6s    2.5x  (diminishing returns)
```

**32 is the sweet spot.** 64 saves only 0.3s over 32 — not worth the extra connection pressure.

Changes made:

1. `ww/git/git_update.py` — default jobs 8 → 32
2. `git config --global submodule.fetchJobs 4` — parallel submodule fetches
3. `git config --global http.postBuffer 524288000` — 500MB buffer for large repos

You can still override per-run: `ww projects update -j 64` or `ww projects update -j 16`.

Also: that 1 failed repo — want me to check which one it is?
