---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复训练100k步
translated: true
type: note
---

好的，以下是基于原始训练配置的命令：

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

具体含义：

- 从第200k步检查点（model_200000.pt）恢复训练
- 运行至300k步（额外100k步）
- 所有学习率设为原始值的0.06倍（与第一次运行结束时相同）
- `--warmup-steps 0 --warmdown-ratio 0` → 学习率恒定，无预热/衰减，全程保持不变
- 批次大小、架构、评估设置与之前相同

大致预计耗时：100k步 × 约1.18秒/步 ≈ 32.8小时

在工作站的tmux中运行：

```
tmux attach -t 14
```

然后粘贴命令。
