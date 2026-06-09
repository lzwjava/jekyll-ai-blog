---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resume Training at Lower LR
translated: false
type: note
---

Here's the corrected command matching your original style:

```
cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train --run=rtx4070-d12-300k --depth=12 --aspect-ratio=64 --head-dim=128 --max-seq-len=2048 --window-pattern=L --device-batch-size=8 --total-batch-size=65536 --num-iterations=300000 --resume-from-step=200000 --warmdown-ratio=0.0 --final-lr-frac=0.05 --embedding-lr=0.018 --unembedding-lr=0.00048 --matrix-lr=0.0012 --scalar-lr=0.03 --weight-decay=0.28 --warmup-steps=0 --eval-every=5000 --core-metric-every=10000 --sample-every=10000 --save-every=10000 --tracker=none
```

Key changes from original:
- `--run=rtx4070-d12-300k` (new run name)
- `--num-iterations=300000` (was 200k, now 300k)
- `--resume-from-step=200000` (was 130k, now 200k)
- All LRs × 0.06: `matrix-lr=0.0012`, `embedding-lr=0.018`, `unembedding-lr=0.00048`, `scalar-lr=0.03`
- `--warmup-steps=0` (no warmup, we're resuming)
- `--warmdown-ratio=0.0` (flat LR, no decay)

ETA: ~33 hours
