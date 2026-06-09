---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以较低学习率恢复训练
translated: true
type: note
---

以下是与您原始风格匹配的更正命令：

```
cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train --run=rtx4070-d12-300k --depth=12 --aspect-ratio=64 --head-dim=128 --max-seq-len=2048 --window-pattern=L --device-batch-size=8 --total-batch-size=65536 --num-iterations=300000 --resume-from-step=200000 --warmdown-ratio=0.0 --final-lr-frac=0.05 --embedding-lr=0.018 --unembedding-lr=0.00048 --matrix-lr=0.0012 --scalar-lr=0.03 --weight-decay=0.28 --warmup-steps=0 --eval-every=5000 --core-metric-every=10000 --sample-every=10000 --save-every=10000 --tracker=none
```

与原始版本相比的关键更改：

- `--run=rtx4070-d12-300k`（新的运行名称）
- `--num-iterations=300000`（原为200k，现为300k）
- `--resume-from-step=200000`（原为130k，现为200k）
- 所有学习率乘以0.06：`matrix-lr=0.0012`，`embedding-lr=0.018`，`unembedding-lr=0.00048`，`scalar-lr=0.03`
- `--warmup-steps=0`（无预热，因为我们从中断点恢复）
- `--warmdown-ratio=0.0`（平坦学习率，无衰减）

预计耗时：约33小时
