---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于策略的REINFORCE微调在GSM8K上的应用
translated: true
type: note
---

该脚本使用在线策略梯度强化学习（on-policy policy-gradient RL）在GSM8K数学应用题上微调预训练（SFT）聊天模型。如文档字符串所述，它标记为"GRPO"，但实际上是简化的REINFORCE：

- **无KL正则化**（无参考模型信任区域）
- **无PPO比率+裁剪**（在线策略下非必需——每次采样仅使用一次）
- **DAPO风格的Token级归一化**：优势值 = `奖励 − 奖励均值`（基于同一问题的样本，不除以标准差）
- 梯度按**有效Token数量**缩放（掩码Token级归一化），而非序列长度

## 流程概述

### 1. 准备工作
- 命令行参数支持日志记录（wandb/mlflow）、运行时配置、模型加载、批次大小、生成参数，以及按参数组设置学习率（嵌入层Adam学习率0.2、反嵌入层Adam学习率0.004、矩阵层Muon学习率0.02 —— NanoChat分组方案）。
- 通过`load_model("sft", ...)`加载SFT模型，并封装入`Engine`以支持批量采样。

### 2. 采样生成器（`get_batch`）
核心数据循环。每步操作：
1. 每个DDP秩（rank）遍历自己的训练子集（`rank_indices`），避免数据重复。
2. 渲染对话补全（用户+助手前缀，保留助手起始标记，删除后续助手文本）。
3. 每道题生成`num_samples`个补全结果，按`device_batch_size`分批避免显存溢出，使用确定性逐步种子。
4. **奖励** = `task.reward(conversation, generated_text)` —— GSM8K验证器（通过比较最后一个数字等，检查模型最终答案与标准答案是否一致）。
5. 用`<|assistant_end|>`标记将所有样本填充至等长（损失计算中掩码处理），构建偏移一个Token的`(输入, 目标)`对，掩码为0处设置`目标 = -1`（忽略索引）——即**提示Token和强制工具使用Token不参与损失计算**。
6. **优势值** = `奖励 − 奖励均值`（基于该问题`num_samples`个样本）。高于问题均值的样本获得正优势（提升概率），低于均值的样本被抑制。

### 3. 评估（`run_gsm8k_eval`）
pass@k评估器：对每个评估问题，采样`k = 1..device_batch_size`个补全结果，通过`task.evaluate`验证正确性，统计前k个结果中至少有一个正确答案的问题数量。各秩协同处理样本；训练循环通过`all_reduce`跨秩汇总，记录pass@k至跟踪器。

### 4. 训练循环
每步针对分配给本秩的每个样本：

1. **策略梯度目标**：计算逐Token对数概率`logp = -model(...)`（负对数似然），则  
   `pg_obj = Σ (logp · 优势值)`（所有Token求和），归一化因子为：  
   `有效Token数 × 采样次数 × 每秩样本数` —— 这是掩码Token级归一化（DAPO风格），使每个Token的有效学习率不随序列长度变化。
2. `损失 = -pg_obj; 损失.backward()` 累积所有样本和采样次数的梯度（中间不执行优化器步骤——整步采样的梯度累加）。
3. **学习率调度**：从`初始学习率比例 × 基础学习率`线性衰减至0，持续`num_steps`步。
4. `优化器.step()` 后执行`梯度清零`。
5. 记录平均奖励/平均生成序列长度（跨秩平均），主进程每`save_every`步保存检查点。

## 有效原因/关键设计选择

| 选择 | 理由 |
|---|---|
| 在线策略，每次采样仅使用一次 | 无需重要性采样比率，无需裁剪 —— 最简单的稳定策略梯度更新 |
| 优势值 = r − μ（无σ） | DAPO：样本方差小除以标准差会放大噪声 |
| Token级归一化 | 长序列不主导梯度；每个有效Token贡献均等 |
| 基于验证器而非学习奖励模型 | GSM8K答案可验证，奖励精确且计算成本低 |
| 忽略索引掩码 | 模型仅训练其自身生成的推理内容，不训练提示或强制Token |
| 梯度整步累积 | 有效批次 = `每步样本数 × 采样次数` 个序列后执行优化器步骤 |

## 快速参考
- 单GPU运行：`python -m scripts.chat_rl`
- 8GPU运行：`torchrun --standalone --nproc_per_node=8 -m scripts.chat_rl -- --run=default`
- 关键参数：`--num-samples`（每问题采样数，决定优势组大小）、`--examples-per-step`（每步总问题数）、`--temperature`/`--top-k`（探索参数）、`--max-new-tokens`（采样长度上限）。

值得注意的简化：它使用`model.state_dict()`保存检查点，但**不保存优化器状态**，因此中途恢复训练会从零开始重新执行学习率调度。