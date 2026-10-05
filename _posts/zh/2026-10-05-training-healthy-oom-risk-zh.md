---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 健康训练，OOM风险
translated: true
type: note
---

已检查 tmux 会话 `1`。以下是完整状态：

## 当前运行 — 健康且正在训练 ✅

**进程：** `python -m scripts.base_train --depth=18 --max-seq-len=1024 --device-batch-size=1 --tracker=none --run=d18-climbmix --core-metric-max-per-task=50 --save-every=250`（PID 3976056，今日 02:59 启动）

| 指标 | 数值 |
| --- | --- |
| 进度 | 步骤 **544 / 3712**（约 14.6%），第 1 个 epoch |
| 损失 | 约 2.97（从初始的 10.4 下降；近期范围 2.82–3.07） |
| 速度 | 约 14,000 tok/s，约 75 秒/步 |
| MFU | 约 99.1%（BF16）— 稳定 |
| 学习率 | 仍为 1.00，尚未衰减 |
| 预计剩余时间 | 约 3,955 分钟 ≈ **66 小时 ≈ 2.7 天**（完成时间约 10 月 8 日） |
| GPU | RTX 4070：使用率 100%，**11.36 / 12.28 GB VRAM（92%）**，60°C，164 W |

**检查点**（`/mnt/data/nanochat-cache/base_checkpoints/d18/`）：已保存步骤 250（08:37）和步骤 500（14:02），每个约 6.8 GB；下次保存为步骤 750。

## 之前发生的情况 ⚠️

回滚日志显示，此会话中先前的一次运行已达到 **步骤 1999/3712（53.85%，损失约 2.68）**，并通过了步骤 2000 的验证（bpb 0.8279）+ 评估套件——然后 在 `boolq` 评估任务（`nanochat/gpt.py` logits softcap，尝试分配 1.51 GiB 但只有 1.16 GiB 空闲）期间 **因 `torch.OutOfMemoryError` 崩溃**。这导致旧运行被终止，您从头重新启动——这就是当前运行回到步骤 544 的原因。

## 风险标志

训练已使用 **92% 的 VRAM**，而步骤 2000 的评估在此基础上运行——同样的 OOM 很可能在 **10 月 6 日约 21:00**（步骤 2000）再次发生。在此之前，请考虑：

- 使用 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`（回溯本身建议）重新启动，或
- 修改评估路径以释放训练内存 / 分块进行评估。

目前无需采取行动——训练正在正常进行。
