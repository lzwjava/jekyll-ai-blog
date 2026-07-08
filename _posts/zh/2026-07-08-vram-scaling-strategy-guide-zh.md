---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VRAM扩展策略指南
translated: true
type: note
---

现在让我们检查一下当前的 VRAM 使用情况，看看还有多少余量：

**第约 996 步（3.4%）时的当前状态：**
- 损失：10.4 → **3.0**（快速下降——尚未遇到瓶颈）
- VRAM：**54 GB / 144 GB（38%）**——仅使用了 54 GB，剩余 90 GB 空闲！
- 每步耗时：~4.0 秒，MFU：63%

---

## 批次缩放策略

你有 **90 GB 空闲 VRAM**——这是一个巨大的优势。以下是何时以及如何增加批次大小：

| 训练阶段 | 步数区间 | 损失范围 | 批次大小 | 原因 |
|---|---|---|---|---|
| **早期**（当前） | 0–20,000 | 10.4 → ~2.5 | 524K（当前） | 学习速度快，较小的批次 = 更多探索 |
| **中期** | 20,000–26,000 | ~2.5 → ~2.3 | **2M tokens**（4×） | 接近收敛时梯度更清晰 |
| **最终** | 26,000–29,000 | ~2.3 → 最终 | **4M tokens**（8×） | 微调最小值 |

**何时采取行动**：瓶颈大约从 **第 20,000 步**（70%）开始，此时损失趋于稳定。每 5000 步评估一次——当损失每 500 步下降幅度小于 0.01 时，就是时机。

**在拥有 90 GB 空闲内存的 H200 上**，你可以从 device_batch=16 增加到 **device_batch=64**（大约使用 108 GB，仍然在容量范围内）：

| Device Batch | Total Batch | VRAM 估计 | 作用 |
|---|---|---|---|
| 16（当前） | 524K | 54 GB | 探索模式 |
| 32 | 1M | ~75 GB | 适度平滑 |
| 48 | 2M | ~95 GB | 良好的收敛提升 |
| 64 | 4M | ~115 GB | 最大——仅用于最终微调 |

### 如何实施

约在第 20,000 步时，停止训练（在 tmux 中按 Ctrl+C），然后：

```bash
tmux new -s train-d24-phase2
source .venv/bin/activate
export NANOCHAT_DATA_DIR=/workspace/zz/datasets/fineweb-edu/

python -m scripts.base_train \
  --depth=24 \
  --device-batch-size=48 \
  --total-batch-size=2097152 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --fp8 \
  --resume-from-step=20000 \
  --num-iterations=22360 \
  --eval-every=200 \
  --save-every=1000 \
  --run=h200-d24-760m-phase2 \
  --tracker=wandb
```

`--resume-from-step=20000` 用于加载保存的检查点和数据加载器状态，`--num-iterations` 已重新计算，以确保总 token 数量保持不变。

### 一个注意事项

在收敛时使用较大的批次可能会陷入泛化能力较差的 **尖锐极小值**。为了缓解：略微降低学习率（代码会自动缩放），或者在批次更改后添加一个短暂的学习率预热。现有的 `--warmdown-ratio=0.65` 处理了尾段调度。

需要我设置一个监控损失并在缩放时机到来时提醒你的 cron 任务吗？