---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resume Training for 100k Steps
translated: false
type: note
---

Got it. Here's the command based on the original training config:

```
cd /mnt/data/nanochat && python -m scripts.base_train \
  --run rtx4070-d12-300k \
  --tracker none \
  --depth 12 \
  --aspect-ratio 64 \
  --head-dim 128 \
  --max-seq-len 2048 \
  --window-pattern L \
  --device-batch-size 8 \
  --total-batch-size 65536 \
  --num-iterations 300000 \
  --resume-from-step 200000 \
  --matrix-lr 0.0012 \
  --embedding-lr 0.018 \
  --unembedding-lr 0.00048 \
  --scalar-lr 0.03 \
  --weight-decay 0.28 \
  --warmup-steps 0 \
  --warmdown-ratio 0.0 \
  --final-lr-frac 0.05 \
  --eval-every 5000 \
  --eval-tokens 41943040 \
  --core-metric-every 10000 \
  --core-metric-max-per-task 500 \
  --sample-every 10000 \
  --save-every 10000
```

What this does:

- Resumes from step 200k checkpoint (model_200000.pt)
- Runs to 300k steps (100k more steps)
- All LRs set to 0.06× their original values (same as end of first run)
- `--warmup-steps 0 --warmdown-ratio 0` → flat LR, no warmup/warmdown, constant throughout
- Same batch size, architecture, eval settings as before

Rough ETA: 100k steps × ~1.18s/step ≈ 32.8 hours

Run it inside tmux on the workstation:

```
tmux attach -t 14
```

Then paste the command.
