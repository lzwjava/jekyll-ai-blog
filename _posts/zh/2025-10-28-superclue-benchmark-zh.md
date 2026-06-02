---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: SuperCLUE：中文大语言模型基准评测
translated: true
type: note
---

SuperCLUE 是一个综合性基准测试套件，旨在评估中文大语言模型（LLMs）。它基于原有的CLUE（中文语言理解评估）基准，将其扩展至评估大语言模型的高级能力，而不仅限于较小模型。由CLUEbenchmark团队开发——该团队汇聚了来自清华大学等研究机构及中国人工智能生态企业的研究人员——SuperCLUE 于2023年首次推出，旨在弥补中文大语言模型与国际标准对比评估的空白。

### 核心特性

- **重点领域**：从四个主要维度评估模型：
  - 语言理解与生成（如阅读理解、文本摘要）
  - 专业技能与知识（如数学推理、编程能力）
  - 智能体能力（如工具调用、任务规划）
  - 安全性（如偏见识别、伦理对齐）
- **结构体系**：划分为12项核心任务，包含如SuperCLUE-Math6等多步骤数学推理数据集
- **目标意义**：助力追踪中国人工智能发展进程，既展现中文模型优势（如文化语境处理），也揭示与GPT系列等国际模型的差距
- **持续更新**：截至2025年中，该基准已用于周期性评估，排行榜显示如Qwen、GLM等中文模型与国际模型的差距正在缩小

该基准测试为开源项目并持续维护，评估结果常通过arXiv论文和GitHub平台共享。

[SuperCLUE：综合性中文大语言模型基准](https://arxiv.org/abs/2307.15020)
[SuperCLUE GitHub仓库](https://github.com/CLUEbenchmark/SuperCLUE)
[ChinAI：SuperCLUE基准——2025年中阶段性评估](https://chinai.substack.com/p/chinai-324-superclue-large-model)
