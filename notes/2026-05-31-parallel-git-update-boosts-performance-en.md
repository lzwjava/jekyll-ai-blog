---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel Git Update Boosts Performance
translated: false
type: note
---

Done. Here's the summary:

```
Before (sequential):  22.1s for 5 repos
After  (8 workers):    4.8s for 5 repos  → 4.6x speedup
```

For your 62-repo update:
- Sequential: ~4.5 minutes (62 × ~4.4s each)
- Parallel -j8: ~35 seconds (62 × 4.4s ÷ 8 workers)

Changes made:

1. `ww/git/git_update.py` — added `ThreadPoolExecutor` with `--jobs/-j` flag (default 8). Parallel git pulls via `as_completed()`. All 12 existing tests still pass.

2. `~/.zsh/completions/_ww` — added completion for `projects update --jobs/-j/--category/-c/--list`.

Usage:
```
ww projects update              # all repos, 8 workers (default)
ww projects update -j16         # more aggressive
ww projects update -j1          # sequential (old behavior)
ww projects update @ai          # category filter + parallel
ww projects update pytorch llama.cpp  # specific repos + parallel
```

The bottleneck is network I/O (git fetch), so threads are the right tool — no need for multiprocessing. Each thread spends almost all its time waiting on the SSH/HTTPS socket, so 8-16 workers saturate the network link nicely without contention.