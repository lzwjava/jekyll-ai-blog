---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练进度快照
translated: true
type: note
---

训练在 `train` tmux 会话中运行顺利。以下是当前快照：

  Iteration:  ~326,960
  最新损失: 2.1948 (iter 326960)
  每步时间:  ~621-622ms (非常稳定)
  MFU:        14.44% (已趋于平稳)

MFU（模型FLOPs利用率）早期从约13.9%上升至14.44%，此后一直保持平稳。损失在约1.5到4.0之间波动，这对逐步损失来说是正常的——更重要的是运行平均值。每步时间稳定在621-622ms，没有出现减速或停滞。
