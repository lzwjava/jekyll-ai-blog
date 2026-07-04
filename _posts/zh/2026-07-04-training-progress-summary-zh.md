---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练进度摘要
translated: true
type: note
---

**训练正在运行**。已执行至第 67/50000 步：

```
step 00067/50000 | loss: 5.89 → 5.90 | lrm: 1.00
dt: 1195ms/step | tok/sec: 54,834
epoch: 1 | total time: 1.14m | eta: 998m (~16.6h)
```

损失从第 58 步的约 6.0 下降到第 67 步的约 5.89 —— 对于词汇量为 32768 的新初始化模型而言（随机初始化损失 = log2(32768) ≈ 15），这是正常的初始下降。

训练在 tmux 会话 **train** 中运行。连接方式：

```
tmux attach -t train
```

随时查看摘要：

```
bash /mnt/data/zz/train_log.sh --summary
```
