---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 326k步训练之旅
translated: true
type: note
---

以下是我们如何达到约326k步的完整历程：

=== ZZ 训练历程 ===

第一阶段：数据收集与工具构建（2026年5月-6月）
仓库最初是一个数据集处理流水线。你构建了脚本来：
- 下载 FineWeb（100B tokens，GPT-3 消融分片）和 Wikimedia 数据转储
- 使用 hf-mirror.com 实现中国地区访问，支持断点续传（progress.json）
- 将数据提取并分词为 uint16 .npy 分片（GPT-2 BPE）

第二阶段：首次小规模运行（FineWeb，125M 模型）
使用 GPT-2 124M 模型在 FineWeb 数据上进行早期训练：
- 配置：12层，12头，768嵌入，学习率3e-4，最大迭代12k
- 损失从10.87下降到3.53，约20k次迭代（train_log_fineweb.txt）
- 步时：约3.9秒/迭代，MFU约11%

第三阶段：NANOCCHAT 运行（286M 模型，6月4-6日）
在 fineweb-edu 上使用更大的模型（286M参数，深度=12，n_embd=768，n_head=6）：
- 在 RTX 4070 上约28.4小时完成87k步
- 验证集 bpb：0.934 → 0.866（稳步提升）
- 吞吐量约55,670 tok/秒
- 在第87,000步干净地完成

第四阶段：760M 运行（MI300X，短暂）
尝试了760M模型运行（记录在 nanogpt_760m_train 日志中），可能是在
租用的 MI300X GPU 上。

第五阶段：GITHUB-CODE 124M（当前，正在运行）
将数据集切换为282个 GitHub 代码的 .npy 分片（27GB 分词后）。
配置：GPT-2 124M，batch=4×1024×8 累积 = 32,768 tok/步，
学习率=6e-4，最大迭代427k → 总计14B tokens。

进度：
  第0步：损失 10.87（随机初始化）
  第25k步：损失约3.6（快速学习）
  第325k步：验证损失 2.7892（刚在325k评估）
  当前：约326,960 / 427,000 = 76.6% 完成

步时开始时约3.9秒，但在 torch.compile 预热后下降到约621毫秒。
MFU 稳定在14.44%。按当前速度，剩余约62k步 × 621毫秒 ≈ 10.7小时。

检查点保存到 /mnt/data/nanoGPT/out-github-code-124m/（1.4GB）。