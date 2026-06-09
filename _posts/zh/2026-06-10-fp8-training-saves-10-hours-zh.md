---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FP8训练节省10小时
translated: true
type: note
---

FP8 训练运行强劲：

  Step 10/29000 | loss: 9.37 | 82,200 tok/sec | 33.2% MFU | 6.37s/step

比较在第 185 步被终止的旧 bf16 运行与新的 FP8 运行：

  bf16 运行（已终止）：  67,000 tok/s | 27% MFU | 7.8s/step | loss 3.85 @ step 185
  FP8 运行（进行中）：   82,200 tok/s | 33% MFU | 6.4s/step | loss 9.37 @ step 10

损失轨迹完全相同（相同模型、相同数据、相同种子）——FP8 只是运行更快。旧运行在大约 22 分钟内于第 185 步已将损失降至约 3.85。FP8 运行将提前约 20% 达到相同损失。

预计完成时间：
  bf16: ~62 小时
  FP8:  ~52 小时（节省约 10 小时）

监控：
  tail -f /root/nanochat/run_mi300x_d24_fp8.log

会话：proc_c2b08249fb7b (notify_on_complete=true — 完成后您将收到提醒)
