---
audio: false
generated: true
image: false
lang: zh
layout: post
title: train/mfu 指标错误为零
translated: true
type: note
---

MLflow DB 运行正常。当前状态：

```
2 runs in the database:
  1. RUNNING  (started Jun 10 ~20:37 UTC)
  2. FINISHED (started Jun 10 ~14:31 UTC)

Latest metrics at step 700:
  train/loss       = 3.707
  train/tok_per_sec = 55,780
  train/mfu        = 0.0        <-- 这不对，应该非零
  train/dt         = 1.175s per step
  total_train_time = 810s (~13.5 min)
```

该数据库处于活跃状态并持续更新。RUNNING 运行任务正在主动记录日志。你遇到的具体问题是什么？是以下哪一项？

1. UI 无法连接到该数据库？
2. `train/mfu = 0.0` 看起来有误？
3. 其他问题？
