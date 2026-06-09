---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muon Momentum Crisis
translated: false
type: note
---

NOT GOOD. Here's the comparison:

```
              Old run (200k)    New run (v2)
              val_bpb  loss    val_bpb  loss
Step 130k     0.780    2.602   0.810*   -
Step 140k     0.865    2.772   0.902    2.888
Current               ~2.56           ~2.91
```

*130k eval differs because eval_tokens changed (524288 vs 41943040)

val_bpb at 140k: 0.902 (WORSE than old run's 0.865). min_val_bpb still 0.780 from the 130k checkpoint — the model hasn't improved at all in 12k steps. Loss flat at ~2.91, not decreasing.

ROOT CAUSE: It's not the LR — it's the Muon momentum.

```
Old run at step 130k: momentum = 0.90 (warmdown complete)
New run:              momentum = 0.97 (flat, never decays)
```

The old run's warmdown decayed momentum from 0.97→0.90. Your optimizer state was calibrated for momentum=0.90. Now it's running at 0.97 — the velocity buffers are too aggressive, causing persistent instability.

This run is unlikely to recover. I'd recommend killing it and restarting with a proper warmdown ratio so momentum decays naturally:

```bash
# Kill current run (Ctrl+C in tmux session 14)
# Then restart from the 130k checkpoint with warmdown-ratio=0.33
# so warmdown starts at step 200k and momentum decays 0.97→0.90 over the last 66k steps

cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train \
  --run=rtx4070-d12-200k-v3 \
  --depth=12 \
  --aspect-ratio=64 \
  --head-dim=128 \
  --max-seq-len=2048 \
  --window-pattern=L \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=200000 \
  --resume-from-step=130000 \
  --warmdown-ratio=0.33 \
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

This gives:

- LR at resume (step 130k): lrm=1.0, effective matrix_lr=0.000354 (matches old run) ✓
- Momentum at resume: 0.97 (same as v2 — brief spike, but LR is low enough to absorb it)
- Momentum at step 200k: 0.90 (matches old run's end state) ✓
- LR at step 200k: lrm=0.05, effective matrix_lr=0.000018 ✓

Want me to kill the current run and start this?
