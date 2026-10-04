---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 核心指标评估实现
translated: true
type: note
---

`nanochat/core_eval.py` 实现了 [DCLM 论文](https://arxiv.org/abs/2406.11794) 中的 **CORE 指标**评估——一套用于评估语言模型在下游任务上表现的基准套件。该模块被 `scripts/base_eval.py` 使用，后者将每个任务的平均准确率汇总为最终的 CORE 分数。

## 功能概述

**1. 提示渲染（3 种任务类型）**——使用 Jinja2 模板构建少样本提示：
- `render_prompts_mc` —— **多项选择**：为每个选项渲染一个提示（问题 + 选项附加）
- `render_prompts_schema` —— **模式**：为每个上下文选项渲染一个提示（上下文 + 固定续文）
- `render_prompts_lm` —— **语言建模**：渲染一对提示，分别 *不包含* 和 *包含* 续文

**2. 分词/批处理辅助函数**：
- `find_common_length` —— 定位分词后提示的公共前缀（MC）或公共后缀（schema），从而只对不同的答案/上下文 token 进行评分
- `batch_sequences_mc/schema/lm` —— 分词，然后计算 `start_idxs`/`end_idxs`，标记每个提示中需要评估的 token 区间
- `stack_sequences` —— 将提示右对齐填充为批处理张量

**3. 评分**（`forward_model`、`evaluate_example`）：
- 对模型进行一次前向计算，计算每个 token 的交叉熵损失（自回归地移动目标）以及 argmax 预测
- **LM 任务**：如果模型 *精确预测* 续文的 *每个 token*，则正确
- **MC/schema**：计算每个选项答案区间的平均损失；如果黄金选项的损失最低，则正确
- 处理少样本采样（确定性种子 `1234 + idx`）、截断至 `model.max_seq_len`，每个示例返回一个布尔值

**4. 分布式评估**（`evaluate_task`）：
- 当在 `torchrun`（`dist.is_initialized()`）下运行时，跨各进程交错分配示例
- 对正确性向量执行 `all_reduce`，然后返回该任务的均值准确率

## 已知问题
该文件中的 TODO 注释指出，除 **SQuAD** 外所有任务均与参考数值吻合，而 SQuAD 的得分为 31%，与参考值 37% 不符。