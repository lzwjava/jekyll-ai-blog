---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 培训进度更新与分析
translated: true
type: note
---

## tmux 7 进度 — fineweb-gpt3 训练

**当前迭代 ~7020 / 19073**（10B token 运行已完成约 37%）。

### 损失曲线（每 500 次迭代的 val loss）

| step | train | val      |
| ---- | ----- | -------- |
| 4500 | 3.34  | 3.30     |
| 5000 | 3.31  | 3.26     |
| 5500 | 3.27  | 3.26     |
| 6000 | 3.23  | 3.25     |
| 6500 | 3.26  | **3.17** |
| 7000 | 3.22  | 3.18     |

健康下降趋势。val 跟随 train，无 overfitting 信号。从 step 6000 到 6500 的 3.25 → 3.17 下降是近期最大单次跳跃——模型仍在学习有用结构，尚未进入平台期。

### 吞吐量

- **~11.11 s/iter** 稳态，每个 eval 周期峰值 **MFU ~12.86%**
- Eval 步骤（每 500 次）耗时约 29 秒——多出的 18 秒用于 eval + checkpoint 保存
- 按 11.11 s/iter 计算，剩余约 12,053 次迭代 → **约 37 小时**到达 `max_iters=19073`

### 发现/观察

1. **训练稳定。** 无 loss 尖峰，无 NaN，未见热节流。根据之前 `nvidia-smi` 数据，GPU 为 66C / 207W。
2. **每个 eval 窗口 MFU 重置**（eval 后立即降至 ~12.07%，又爬升至 12.86%）。这只是移动平均热身——并非真正回归。
3. **已用 ~7.5 GB / 12 GB**——确认了之前的显存分析。`batch_size=4 → 6` 的余量仍然存在，但**不应在运行中途更改**，因为这会破坏 LR schedule 与 optimizer steps 的关系。留到下一次运行再改。
4. **每 500 次迭代保存 checkpoint**（`always_save_checkpoint=True`）。目前约保存了 14 个 checkpoint——如果只保留一个文件，请确保 `out-fineweb-gpt3/` 没有填满磁盘（nanoGPT 会覆盖 `ckpt.pt`，所以应该没问题）。
5. **当前损失**：对于在 FineWeb-Edu 上运行 10B token 约 37% 的 124M 模型，约 3.18 val 是合理的。GPT-2 124M 在 OpenWebText 上通常在完整训练结束时 val 落在 2.85–2.90 左右，所以还有下降空间。

### 简要总结

运行状态良好，已完成约 37%，loss 曲线正常，以当前速度还需约 37 小时。无需干预。
