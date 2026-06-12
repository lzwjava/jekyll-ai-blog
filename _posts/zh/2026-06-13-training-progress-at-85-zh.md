---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练进度85%
translated: true
type: note
---

训练在 tmux 34 中运行良好。当前状态如下：

  Progress:  85% (2247/2656 steps), ~1:35 remaining
  Epoch:     1.69
  Tokens:    ~27.4M processed
  Loss:      1.45 (latest), trending around 1.43-1.52 range
  Accuracy:  ~64.9% mean token accuracy
  LR:        1.27e-05 (decaying nicely via cosine schedule)
  Grad norm: 0.035 (stable)

训练看起来健康——损失稳定在 1.4-1.5 范围内，梯度范数低且稳定（~0.03），学习率正处于最终的余弦衰减阶段。大约 1.5 小时后完成。