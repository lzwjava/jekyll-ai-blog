---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving LR Spike in Resumed Training
translated: false
type: note
---

Now I have the full picture. Here's what happened and the corrected command:

---

The 200k run completed but val_bpb DEGRADED: 0.780 (step 130k) → 0.865 (step 140k) → 0.801 (step 200k). The min_val_bpb never improved past the 130k checkpoint.

The problem: the 130k run's warmdown was COMPLETE (lrm=0.05). When you started the 200k run with the same LR params, the schedule recalculated based on 200k total — warmdown started at step 70k instead of 45k. At step 130k the new lrm was 0.537 (vs 0.05 in the old run). That's a ~10x LR spike that wrecked the optimizer state.

Here's the corrected approach: resume from the 130k checkpoint (best val_bpb=0.780) and scale ALL lr params by final_lr_frac (0.05) so the effective LR matches exactly where the 130k run ended:

```
cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train \
  --run=rtx4070-d12-200k-v2 \
  --depth=12 \
  --aspect-ratio=64 \
  --head-dim=128 \
  --max-seq-len=2048 \
  --window-pattern=L \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=200000 \
  --resume-from-step=130000 \
  --warmdown-ratio=0 \
  --final-lr-frac=0.05 \
  --embedding-lr=0.015 \
  --unembedding-lr=0.0004 \
  --matrix-lr=0.001 \
  --scalar-lr=0.025 \
  --weight-decay=0.28 \
  --warmup-steps=40 \
  --eval-every=5000 \
  --core-metric-every=10000 \
  --sample-every=10000 \
  --save-every=10000 \
  --tracker=none
```

The math:

```
Original LR params × final_lr_frac = scaled LR (matches step 130k exactly)
  embedding:   0.3  × 0.05 = 0.015
  unembedding: 0.008 × 0.05 = 0.0004
  matrix:      0.02 × 0.05 = 0.001
  scalar:      0.5  × 0.05 = 0.025

--warmdown-ratio=0: flat LR for all 70k new steps (no decay)
--warmup-steps=40: brief ramp since optimizer state already equilibrated
--resume-from-step=130000: resume from the BEST checkpoint
```

Why this works:

- No LR spike: scaled LRs match the 130k run's final values exactly
- Flat schedule: warmdown-ratio=0 keeps LR constant, no schedule recalculation
- Optimizer state (Adam v_t, Muon momentum) stays in sync
- Muon momentum stays at 0.97 (flat, since no warmdown phase)

Clean old checkpoints first to make room:

```
ssh lzw@192.168.1.36 "cd /home/lzw/.cache/nanochat/base_checkpoints/d12/ && ls -1 | grep -v '130000' | xargs rm -v && df -h /"
```
