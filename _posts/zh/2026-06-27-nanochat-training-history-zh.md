---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat训练历史
translated: true
type: note
---

以下是您之前的 nanochat 训练的完整情况：

=== 训练历史总结 ===

您运行了多个训练实验。以下是具体情况：

--- 1. d8 基础模型（2 节点 CPU 分布式，6 月 2 日） ---
   - 模型：depth=8，512 dim，4 heads，seq_len=1024
   - 训练至 step 1000（CPU，2 节点），val_bpb = 1.64
   - 在 RTX 4070 上继续训练至 step 5000，val_bpb = 0.99
   - 总训练时间：~26 分钟（RTX 4070 部分）

--- 2. d12 基础模型（RTX 4070，6 月 7-10 日） ---
   - 模型：depth=12，768 dim，6 heads，seq_len=2048
   - 从 step 130,000 恢复训练，训练至 step 200,000
   - 最佳 val_bpb：0.7800（step 130k）
   - 最终 val_bpb：0.8534（step 200k）
   - 总训练时间：RTX 4070 上约 65 小时
   - 批量大小：65,536 tokens，学习率：0.001（Muon），embedding 学习率：0.015

--- 3. d12-fresh-fa2（RTX 4070，6 月 10 日） ---
   - 全新的 d12 模型，使用 Flash Attention 2，seq_len=2048
   - 训练 5000 步，val_bpb = 0.928
   - 总时间：~1.6 小时（短测试运行）

--- 4. d4 基础模型（2 节点 CPU，6 月 11 日） ---
   - 微型模型：depth=4，seq_len=512，仅 20 步
   - val_bpb = 4.23（几乎未训练，仅为测试）

--- 5. d8 SFT（RTX 4070，6 月 2 日） ---
   - 使用 SFT 微调 d8 模型
   - 训练 188 步，val_bpb = 0.822（SFT 损失）
   - ChatCORE 指标：0.0037（基本为随机）

=== 结果分析 ===

d12 模型是您的主要训练成果。结果如下：

  CORE 指标（d8，step 5k）：0.0815（非常弱，随机约为 0）
  目标（GPT-2）：0.2565

d12 模型达到了 val_bpb=0.78，对于 12 层模型来说还算不错，但距离 GPT-2 的能力（CORE 0.2565）仍有很大差距。d8 模型太小，无法发挥作用。在 d8 上进行的 SFT 产生了 0.0037 的 ChatCORE，基本是随机的——基础模型不够好，SFT 也无能为力。

作为参考，Karpathy 的 speedrun 使用 depth=24 和 8×H100，大约 2 小时即可达到 GPT-2 水平。您的 RTX 4070（12GB VRAM）只能容纳较小的模型。RTX 4070 上的 d12 模型花费了 65 小时，仍未达到 GPT-2 水平。

想尝试用 SFT 微调 d12 检查点，还是训练一个新模型？