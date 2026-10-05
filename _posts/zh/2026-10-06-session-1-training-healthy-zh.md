---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第一节 健康训练
translated: true
type: note
---

**Session 1 训练状态健康** — 它刚刚在 step-1000 里程碑完成了定期评估（eval），因此日志暂停了一下：

- **进度：** step 999/3712 已完成（26.91%），刚刚输出 `Step 01000 | Validation bpb: 0.882241`
- **损失：** ~2.8–2.9（平滑后），验证 bpb 0.882
- **速度：** 75.2 秒/步，约 13.9k tok/s，**bf16 MFU 98.7%**
- **预计剩余时间：** 约 3420 分钟（约 57 小时）；总计已运行约 22 小时
- **资源：** GPU 利用率 98%（10.9 GB），进程处于 R 状态，CPU 满载核心——无停滞

约 10 分钟的静默是周期性的 `--eval-every=250` 验证过程（42M tokens）。接下来它会写入 step-1000 的 checkpoint（约 5 GB，与 250/500/750 的 checkpoint 一样存放在 `/mnt/data/nanochat-cache/base_checkpoints/d18`），然后训练日志会继续输出。