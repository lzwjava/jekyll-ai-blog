---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最大化GPU内存的安全使用
translated: true
type: note
---

## 分析：将 4070 显存从约 7.5 GB 推至约 10–11 GB

### 显存来源

在 `batch_size=4, block_size=1024` 时，占用 7538 MiB。大致如下：

- **固定部分**：权重 + 梯度 + AdamW 状态（m, v）≈ 约 2 GB（针对 124M 参数）
- **激活值**：剩余部分（约 5.5 GB），随 `batch_size` 线性增长，随 `block_size` 呈近似平方增长

因此每单位 `batch_size` 的激活值约 1.4 GB。要达到约 10.5 GB，大约需要 **增加 3 GB 激活值 → batch_size ≈ 6**，如果激进一点可以到 7。

### 主要杠杆：`batch_size`（第 15、17 行）

保持每步 token 数（约 524,288）不变，这样学习率调度 / `warmup_iters` / `max_iters` 无需重新调整：

| `batch_size` | `gradient_accumulation_steps` | 每步 token 数 | 预计显存占用 |
| ------------ | ----------------------------- | ------------- | ------------ |
| 4（当前）    | 128                           | 524,288       | 7.5 GB       |
| 6            | 85 或 86                      | ~528K         | ~10 GB       |
| 8            | 64                            | 524,288（精确）| 12 GB 上很可能 OOM |

我会从 **`batch_size=6, gradient_accumulation_steps=86`** 开始，并关注 `nvidia-smi`。如果还有余量，尝试 7。使用 6 时每步 token 数不会完全相同——没关系，学习率调度对百分之几的偏差具有鲁棒性。

### 为什么不使用其他杠杆

- **`block_size`**：与 GPT-2 124M 架构以及数据的 tokenization / sharding 方式绑定。不要改动。
- **`n_layer / n_head / n_embd`**：会改变模型，不仅仅是显存。
- **`compile=True`**：已开启。
- **精度**：nanoGPT 在 `train.py` 中默认已使用 bf16/AMP —— 可验证，但无需修改配置。

### 注意事项

- 显示 / Xorg 占用约 115 MiB，因此可用预算约为 12,160 MiB，而非 12,288。
- 首次 `torch.compile` 步骤会显存尖峰；如果仅在编译时 OOM，这不是稳态问题，但仍然无法运行。请保守处理。
- 从 128 降到 86 个梯度累积步骤意味着 **每个 wall-clock 秒内的优化器更新次数减少**，但 **有效 batch 相同**，因此损失曲线应保持一致。每步吞吐量（token/秒）预计会略有提升，因为每个 token 的 Python/PyTorch 开销减少。

### 总结

将 `batch_size` 从 4 提升到 6，`gradient_accumulation_steps` 从 128 降到 86。其他保持不变。预计显存约 10 GB，吞吐量略有提升。
