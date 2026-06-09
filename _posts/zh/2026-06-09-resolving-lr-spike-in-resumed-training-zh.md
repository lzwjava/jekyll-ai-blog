---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复训练中的学习率尖峰问题
translated: true
type: note
---

现在我掌握了全局。以下是发生的事情和修正后的命令：

---

200k 运行已完成，但 val_bpb 退化了：0.780（第130k步）→ 0.865（第140k步）→ 0.801（第200k步）。min_val_bpb 从未超过第130k检查点。

问题：130k 运行的 warmdown 已完成（lrm=0.05）。当你使用相同的 LR 参数启动 200k 运行时，调度器基于 200k 总数重新计算——warmdown 从第70k步开始，而不是第45k步。在第130k步时，新的 lrm 为 0.537（而旧运行中为 0.05）。这是一个约 10 倍的 LR 尖峰，破坏了优化器状态。

以下是修正方法：从第130k检查点（最佳 val_bpb=0.780）恢复，并将所有 lr 参数按 final_lr_frac（0.05）缩放，使得有效 LR 与 130k 运行结束时的值完全匹配：

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

数学运算：

```
原始 LR 参数 × final_lr_frac = 缩放后的 LR（与第130k步完全匹配）
  embedding:   0.3  × 0.05 = 0.015
  unembedding: 0.008 × 0.05 = 0.0004
  matrix:      0.02 × 0.05 = 0.001
  scalar:      0.5  × 0.05 = 0.025

--warmdown-ratio=0：所有70k新步的 LR 保持平坦（无衰减）
--warmup-steps=40：简短预热，因为优化器状态已经均衡
--resume-from-step=130000：从最佳检查点恢复
```

为何有效：

- 无 LR 尖峰：缩放后的 LR 与 130k 运行结束时的值完全匹配
- 平坦调度：warmdown-ratio=0 使 LR 恒定，无调度重新计算
- 优化器状态（Adam v_t，Muon momentum）保持同步
- Muon momentum 保持在 0.97（平坦，因为无 warmdown 阶段）

先清理旧的检查点以腾出空间：

```
ssh lzw@192.168.1.36 "cd /home/lzw/.cache/nanochat/base_checkpoints/d12/ && ls -1 | grep -v '130000' | xargs rm -v && df -h /"
```
