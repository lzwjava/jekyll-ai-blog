---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training crashed, no checkpoint, restart needed
translated: false
type: note
---

There's no tmux session `a` — you have sessions **`0`** (mihomo proxy) and **`1`** (the training). The train job was in session `1`, and **it has already crashed**:

```
torch.OutOfMemoryError: CUDA out of memory ... during CORE metric evaluation
```

**What happened**
- Command that was running (recovered from the process list / pi session logs):
  ```bash
  NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
      --depth=18 --max-seq-len=1024 --device-batch-size=2 --tracker=none --run=d18-climbmix
  ```
- It reached **step 2000 / 3712 (~54%, ~32h in)**, then OOM'd inside `evaluate_core()` at the CORE-metric checkpoint (`--core-metric-every` defaults to 2000). The GPU now only has desktop processes left — the job is dead.
- ⚠️ **No checkpoint exists for this run.** `/mnt/data/nanochat-cache/base_checkpoints/d18/` only has the 5-step smoke test (`save-every` defaults to `-1` = save only at the end). So a restart means **training from step 0**.

**How to restart**

```bash
tmux attach -t 1
```

then in that pane:

```bash
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --save-every=250
```

**Important — it will otherwise crash again the same way.** The CORE eval OOMs because the training model + optimizer (~7.8 GiB) are still resident while eval logits need another ~1.5 GiB on your 11.6 GiB card, and CORE eval also re-runs at the *final* step (3712). Pick one:

1. **Free VRAM first** — close GPU-using apps (Xorg alone holds ~1.1 GiB, plus browser/Chrome tabs). Eval only needed ~0.4 GiB more than was free.
2. **Lower eval memory**, e.g. add `--core-metric-max-per-task=50` (fewer/slimmer eval batches), or disable it entirely with `--core-metric-every=-1`.
3. **Reduce training footprint**: `--device-batch-size=1`.

I'd strongly recommend `--save-every=250` regardless, so a future crash doesn't cost you another 30+ hours.