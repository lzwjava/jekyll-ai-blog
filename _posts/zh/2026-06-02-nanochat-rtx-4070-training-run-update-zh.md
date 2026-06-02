---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat RTX 4070 训练运行更新
translated: true
type: note
---

Nanochat 正在 RTX 4070 上运行：

  GPU：      RTX 4070 — 2.7 GB / 12 GB VRAM 已使用，利用率 99%
  模型：    depth=8（约 4000 万参数），bf16
  吞吐量：  约 103K tok/秒
  损失：     7.73 → 6.22（步骤 81/5000）
  预计剩余时间：预训练约 26 分钟，然后 SFT（约 8 分钟），总计约 35-40 分钟

在工作站的 tmux 会话 `nanochat` 中运行。日志位于 `/mnt/data/nanochat/run_rtx4070.log`。

注意：仅使用了 2.7 GB VRAM — 你可以轻松增加到 `--depth=12` 或 `--depth=16` 以获得更大的模型。d8 只是一个快速演示运行。你是想让它完成，还是用更大的模型重新启动？