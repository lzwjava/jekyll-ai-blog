---
audio: false
generated: true
image: false
lang: zh
layout: post
title: d18-climbmix训练运行进度报告
translated: true
type: note
---

## 进度报告

**不存在名为 `a` 的 tmux 会话。** 当前活跃会话为 `0` 和 `1`，两者都连接到同一个训练终端（`pts/10`），因此显示完全相同的输出。当前正在运行的训练任务为：

### 🏃 训练运行：`d18-climbmix`（nanochat）

- **命令：** `./.venv/bin/python -m scripts.base_train --depth=18 --max-seq-len=1024 --device-batch-size=2 --tracker=none --run=d18-climbmix`
- **状态：** 运行中（PID 1682358，于 Sep 29 启动，CPU 耗时约 1632 分钟）

| 指标 | 数值 |
| --- | --- |
| 进度 | **step 1585 / 3712（42.70%）**，epoch 1 |
| 损失 | ~2.86（稳定下降） |
| 学习率乘数 | 0.89 |
| 每步耗时 | ~58.2 秒/步 |
| 吞吐量 | ~18,028 tok/秒 |
| BF16 MFU | 127.6% |
| 已用总时间 | ~1,528 分钟（约 25.5 小时） |
| **预计剩余时间** | **~2,063 分钟（约 34.4 小时）** |

### 🎮 GPU（RTX 4070）

- **利用率：** 100%
- **显存：** 11,072 / 12,282 MiB（已用 90%）
- **温度：** 65°C
- **功耗：** 193 W

### ⚙️ 背景信息

- 32 个 Torch `_inductor` 编译工作线程已启动（此编译训练循环的正常行为）。
- 一切正常：GPU 持续满载，损失平滑下降，输出中无错误。

是否需要我检查 `/mnt/data/nanochat` 下的检查点/日志文件（例如最新保存的检查点、评估指标）以获取更多详情？
