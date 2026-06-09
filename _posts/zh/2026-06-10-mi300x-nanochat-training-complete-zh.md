---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X NanoChat训练完成
translated: true
type: note
---

一切运行正常。以下是摘要：

============================================================
  NANOCCHAT 760M 训练 - MI300X 设置完成
============================================================

已完成的工作：
  1. 克隆 nanochat（Karpathy 的 LLM 训练框架）
  2. 使用 ROCm PyTorch 2.9.1+rocm6.4 设置 Python 虚拟环境
  3. 下载 31 个 ClimbMix-400B 数据集分片（约 250 亿 token）
  4. 训练 BPE 分词器（32,768 词表）
  5. 验证模型在 MI300X 上构建和训练
  6. 在后台启动完整训练运行

模型配置：
  架构： depth=24, dim=1536, heads=12, head_dim=128
  参数： 7.6 亿（transformer）+ 6.04 亿（值嵌入）= 总计 13.8 亿
  数据集： ClimbMix-400B（FineWeb 的继任者）
  训练： 29,000 步，批次=524,288 token/步
  Token 数： 约 152 亿（Chinchilla 最优：20 倍参数）

性能（MI300X）：
  吞吐量： 约 68,000 token/秒
  每步时间： 约 7.7 秒
  MFU： 约 27.5%（SDPA 回退，AMD 上无 FA3）
  峰值显存： 约 105 GB / 192 GB
  预计总时长： 约 62 小时

创建的文件：
  /root/nanochat/run_mi300x_d24.sh           # 完整流水线（预训练 + SFT + 评估）
  /root/nanochat/run_mi300x_d24_pretrain.sh  # 仅预训练
  /root/nanochat/run_mi300x_d24.log          # 训练日志（实时）

后台进程：
  会话： proc_c4c8f9ccdff7
  进程 ID： 272714
  状态： 运行中（损失下降：前 8 步从 10.4 降至 9.6）

监控：
  tail -f /root/nanochat/run_mi300x_d24.log

检查点：
  ~/.cache/nanochat/base_checkpoints/d24/
  （每 5000 步保存一次）

恢复（若崩溃）：
  ./run_mi300x_d24_pretrain.sh --resume-from-step=<最后步数>

训练完成后：
  python -m scripts.chat_cli -p '为什么天空是蓝色的？'
  python -m scripts.chat_web