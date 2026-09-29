---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training hasn't started; still compiling.
translated: false
type: note
---

## Findings

There are 2 tmux sessions:

- `0` — running `mihomo` (your proxy/VPN, just traffic logs, irrelevant)
- `1` — the training run

**Training has NOT started yet.** It's still in the one-time `torch.compile` startup phase.

### What's happening in session 1

The run is `scripts/base_train.py --depth=18 ... --run=d18-climbmix` (a 700M param model, 18 layers). It launched at **15:21** and has been running **~4 minutes**, currently stuck at the last log line:

```
W0929 15:21:26 ... Not enough SMs to use max_autotune_gemm mode
```

Everything before that is just config printout. Since then it's inside `torch.compile(model, dynamic=False)` → PyTorch Inductor tracing/compiling + autotuning the entire model graph.

### Why it's "slow" (but not hung)

- It **is actively working**: main PID `1682358` is pegged at **103% CPU** (single-threaded inductor codegen), GPU is at **99% util** / 172 W, and VRAM is slowly climbing (4318 → 4343 MiB). A hung process would be idle.
- This is the **first compile with no cache**: `~/.cache/torch/inductor/` doesn't exist yet, so there's no kernel cache to reuse. Full-graph compile of a 700M model with Flash-Attention-3 + FP8 on an RTX 4070 typically takes **5–20 min** on first run. Subsequent runs will reuse the cache and start in seconds.
- The `Not enough SMs to use max_autotune_gemm` line is just a **warning** (4070 has 46 SMs, below the threshold for the aggressive GEMM autotune) — it falls back to a lighter tuning mode. Not an error.
- Bonus inefficiency: it spawned 32 inductor compile workers but they're mostly idle (0% CPU), because the graph codegen in the main process is single-threaded — that's normal, the workers only kick in for parallel triton codegen.

### Bottom line

Nothing is wrong — just wait it out. The progress bar will appear once compilation finishes and the first step starts. First-step output will show `step ... loss ...` and then it's training.

If you want, I can help speed up future startups by:

1. Setting a persistent `TORCHINDUCTOR_CACHE_DIR` (e.g. under `/mnt/data/nanochat-cache/`) so the compile cache is reusable.
2. Disabling/reducing autotune (`max_autotune=False` / coordinate-descent off) to cut first-compile time at the cost of a few % throughput.

Want me to monitor until the first training step appears, or apply any of the cache fixes?
