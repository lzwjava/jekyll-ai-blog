---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型训练完成
translated: true
type: note
---

训练完成！

  状态：已完成 — 步骤 130,000/130,000
  总耗时：2,549.86 分钟（约 42.5 小时）
  验证集 bpb：0.780026（最小值）
  峰值显存：9,443.99 MiB
  检查点路径：/home/lzw/.cache/nanochat/base_checkpoints/d12/model_130000.pt

评估结果（CORE 指标：0.1916）：

  hellaswag（10-shot）：        0.43
  winograd（0-shot）：          0.62
  winogrande（0-shot）：        0.54
  boolq（10-shot）：            0.585
  bigbench_cs_algorithms：     0.34
  squad（10-shot）：            0.27
  coqa（0-shot）：              0.26
  agi_eval_lsat_ar（3-shot）：  0.21
  bigbench_dyck_languages：    0.17
  bigbench_operators：         0.14
  bigbench_repeat_copy_logic： 0.00
  bigbench_language_id：       0.195

生成的样本看起来连贯但存在重复（这是 286M 模型的典型特征）。检查点已保存，可用于对话或进一步评估。