---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 纳米GPT竞速：GPT-2模型的快速训练
translated: true
type: note
---

这里是 **NanoGPT 速通** 代码库——一项旨在 8x H100 GPU 上以最快速度训练 GPT-2 的协作优化挑战。目标：在 FineWeb 验证集上达到 3.28 的交叉熵损失。当前记录已突破 90 秒（原始基准为 45 分钟）。

主要内容：

- `train_gpt.py` — 用于 GPT-2 Small（约 1.24 亿参数）的主训练脚本。包含模型定义、自定义优化器（Muon + Adam 混合）及完整训练循环。
- `train_gpt_medium.py` — 类似脚本，但用于 GPT-2 Medium（约 3.5 亿参数）。
- `triton_kernels.py` — 自定义 Triton GPU 内核，用于高效矩阵运算、融合 ReLU² 及软上限交叉熵。
- `data/` — 用于下载/预处理 FineWeb 数据集（10B 或 100B token 版本）的脚本，使用 GPT-2 分词器进行分词。
- `evals/hellaswag.py` — HellaSwag 评估基准。
- `records/` — 包含 Small 赛道的 89 条实验记录和 Medium 赛道的 18 条记录，记录了从 2024 年 6 月到 2026 年 3 月期间优化策略的演进过程。
- `run.sh` — 使用 `torchrun` 启动 8 个进程的启动脚本。

优化内容广泛：旋转嵌入、QK 归一化、ReLU² 激活函数、FP8 矩阵乘法、带滑动窗口的 Flash Attention 3、跳跃连接、稀疏注意力门控、双元哈希嵌入、批大小/序列长度调度等。每条 `records/` 记录都详细说明了变更内容及其带来的加速效果。
