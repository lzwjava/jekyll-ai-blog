---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Training Restart Command and Changes
translated: false
type: note
---

Here's the full restart command (run inside tmux session `1`):

```bash
tmux attach -t 1
```

Then in the pane:

```bash
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

What changed vs. the original command:

- `--core-metric-max-per-task=50` — slimmer CORE eval batches (was default 500), avoids the OOM at step 2000 / final step
- `--save-every=250` — checkpoints every 250 steps so a crash doesn't cost the whole run again (only directory: `/mnt/data/nanochat-cache/base_checkpoints/d18/`)

Note: this restarts from **step 0** — the crashed run never saved a checkpoint.

Want me to send these commands into the tmux pane directly for you?
