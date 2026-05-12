---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 健康培训快照
translated: true
type: note
---

看起来健康——训练运行正常。状态快照：

|                |                                                                      |
| -------------- | -------------------------------------------------------------------- |
| Process        | PID 1200744, running 1m34s, 88% CPU, alive                           |
| GPU            | 7.5 / 12.3 GB VRAM (~4.8 GB headroom), 100% util, 64°C               |
| Params         | 123.59 M ✓ (matches GPT-2 124M)                                      |
| Optimizer      | fused AdamW ✓                                                        |
| Shards         | train=1407, val=1 ✓                                                  |
| Step 0 eval    | train loss 11.0040, val loss 11.0031 ✓ (matches `ln(50304) ≈ 10.83`) |
| iter 0         | 17.16 s (includes warmup; subsequent iters drop to ~11 s)            |
| Last log write | 75 s ago — we're mid-iter, no print yet                              |

为什么没有最近的日志行？`log_interval=20`，因此下一次打印将在迭代 20 进行。以每个迭代约 11 秒计算，那大约是运行开始后的 220 秒（从进程开始约 3.5 分钟）——应该会在接下来的一两分钟内出现。

无需操作。一切正常。大约 5 分钟后回来查看第一个 `iter 20:` 行并确认稳态每迭代时间。