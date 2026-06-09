---
audio: false
generated: true
image: false
lang: zh
layout: post
title: μ子动量危机
translated: true
type: note
---

不理想。以下是对比：

```
              旧运行 (200k)    新运行 (v2)
              val_bpb  loss    val_bpb  loss
步骤 130k     0.780    2.602   0.810*   -
步骤 140k     0.865    2.772   0.902    2.888
当前                 ~2.56           ~2.91
```

*130k 评估差异源于 eval_tokens 的变化（524288 vs 41943040）

140k 步的 val_bpb：0.902（比旧运行的 0.865 更差）。min_val_bpb 仍为 0.780，来自 130k 检查点——模型在 12k 步中完全没有改善。损失值稳定在约 2.91，未见下降。

根本原因：不是学习率的问题——是 Muon 动量的问题。

```
旧运行在步骤 130k：动量 = 0.90（衰减完成）
新运行：              动量 = 0.97（保持不变，从未衰减）
```

旧运行的衰减过程将动量从 0.97 衰减到 0.90。你的优化器状态是以动量=0.90 为基准校准的。现在它以 0.97 运行——速度缓冲区过于激进，导致持续不稳定。

这次运行不太可能恢复。建议终止当前运行，并用合适的衰减比率重新启动，使动量自然衰减：

```bash
# 终止当前运行（在 tmux 会话 14 中按 Ctrl+C）
# 然后从 130k 检查点重新启动，设置衰减比率=0.33
# 这样衰减从步骤 200k 开始，动量在最后 66k 步中从 0.97 衰减到 0.90

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

这将提供：

- 恢复时的学习率（步骤 130k）：lrm=1.0，有效 matrix_lr=0.000354（与旧运行一致）✓
- 恢复时的动量：0.97（与 v2 相同——短暂上升，但学习率足够低以吸收冲击）✓
- 步骤 200k 时的动量：0.90（与旧运行的最终状态一致）✓
- 步骤 200k 时的学习率：lrm=0.05，有效 matrix_lr=0.000018 ✓

需要我终止当前运行并启动这个方案吗？
