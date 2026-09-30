---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练运行已完成46%
translated: true
type: note
---

没有名为`a`的tmux会话——会话是`0`（窗口`mihomo`）和`1`（窗口`./.venv/bin/python`）。两者目前都显示相同的训练日志。以下是最新步骤的当前进度：

**当前状态：**
- **Step:** 01708 / 03712 (**46.01%**)
- **Loss:** 2.6921 (近期范围 ~2.62–2.75)
- **LR multiplier:** 0.84
- **Time per step:** ~58.16s
- **Throughput:** ~18,028 tok/sec
- **BF16 MFU:** 127.60%
- **Epoch:** 1
- **Total time elapsed:** 1646.97 分钟 (~27.4 小时)
- **ETA:** 1943.8 分钟 (~32.4 小时剩余)

因此，运行进度大约为**46%**，还剩约**32小时**。损失在低2.6到中2.7之间徘徊，并且在最后几步中似乎大致进入了平台期。