---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub代码GPT-2训练管道
translated: true
type: note
---

以下是完整的流水线摘要：

=== /mnt/data/zz — GitHub代码训练流水线 ===

步骤1：下载（来自HuggingFace的codeparrot/github-code）
- 脚本：scripts/download/download_github_code.py
- 使用wget从HF拉取parquet分片
- 目前已下载38个分片（约11GB），目标为100GB
- 输出：datasets/github-code/train-00000-of-01126.parquet ...

步骤2：分词（通过tiktoken实现的GPT-2 BPE）
- 脚本：scripts/extract/tokenize_github_code.py
- 读取parquet文件的'content'列，使用tiktoken gpt2进行编码
- 写入包含1亿个token的.npy分片（uint16格式）
- 第一个分片作为验证集，其余作为训练集
- 创建带有edufineweb_前缀的符号链接，以便nanoGPT识别
- 输出：datasets/github-code-tok/
  - 140个训练分片 + 1个验证分片
  - 139.7亿训练token，1亿验证token
  - 总计27GB

步骤3：训练（nanoGPT，当前在tmux会话"train"中运行）
- 配置：nanoGPT/config/train_github_code_124m.py
- GPT-2 124M（12层，12个注意力头，768维嵌入）
- 批次大小4 × 1024，梯度累积8 = 每次迭代32768个token
- 427000次迭代 × 32768 = 约140亿token（覆盖全部数据）
- 当前进度：迭代14000 / 427000（约3.3%）
- 当前最佳验证损失：5.87
- 预计还需约5天完成
- 检查点：out-github-code-124m/ckpt.pt（1.49GB）

最近提交记录：
  79273b9 功能（训练）：为RTX 4070上的github-code添加GPT-2 124M配置
  c0672b7 重构（提取）：简化分词逻辑
  0f9416d 杂项（微调）：添加合并脚本，忽略*.gguf文件
  336bcef 新增github-code下载和分词脚本

注意：1126个parquet分片中仅下载了38个（目标100GB中的11GB）。但分词已产生约140亿token，恰好达到训练配置的目标。因此本次运行的流水线已完成——如需更多数据，可后续下载更多分片。