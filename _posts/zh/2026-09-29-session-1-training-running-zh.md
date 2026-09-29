---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第一节跑步训练
translated: true
type: note
---

训练正在运行中。Session 1 已通过编译，正在训练中。

## 进度（session 1, pane 0）

- **编译完成** — validation 已运行：`Step 00000 | Validation bpb: 3.171`
- **当前在 step 20 / 3712**（0.54%），loss 平稳下降：**10.40 → 6.85**
- LR 仍在预热中（`lrm: 0.53`，正在向 1.0 攀升）

### 吞吐量

- **~17.9k tok/sec**，**~127% bf16 MFU**（超过 100% 是因为它是针对 bf16 峰值 FLOPS 测量的，而实际使用的是 FP8/FA3 — 这是正常的）
- **~58.4 秒/step**（每 step 包含 512 个 grad-accum micro-batches）

### ETA

- 全部 3712 步约需 **~60 小时**（`eta: 3601m`）

### 一切看起来正常

- Loss 曲线符合预期（早期快速下降）。
- 没有错误，`pq: 0 rg: N` 计数器正常递增。

有一点值得注意：**~58 秒/step 偏慢**，主要是因为每个 micro-batch 很小（2×1024 tokens），而且每个 micro-batch 可能有固定的 overhead。如果你需要，我可以调查是否可以通过提高 `--device-batch-size` 或减少 accumulation overhead 来缩短那约 60 小时的 ETA。需要我深入分析 step 耗时分解吗？
