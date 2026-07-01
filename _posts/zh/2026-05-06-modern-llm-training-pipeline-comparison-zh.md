---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 现代大语言模型训练流程比较
translated: true
type: note
---

## llmTrain

这是一个 **教育性端到端 LLM 训练流程** —— 从原始文本训练 BPE 分词器，然后从头训练一个约 1 亿参数的 Transformer。该模型（"MiniLLM-0.1B"）已发布在 HuggingFace Hub 上。

---

## 对比 nanoGPT

| 方面 | **nanoGPT** | **llmTrain** |
| --- | --- | --- |
| **架构** | 经典 GPT-2（学习式位置嵌入，GELU） | 现代：RoPE + SwiGLU + 预归一化 |
| **注意力** | 手动注意力计算 | 通过 `scaled_dot_product_attention` 实现的 Flash Attention |
| **位置编码** | 学习式绝对嵌入 | 旋转位置编码（RoPE） |
| **激活函数** | GELU | SwiGLU（门控线性单元） |
| **分词器** | 使用 GPT-2 分词器（tiktoken） | 从头训练自己的 BPE |
| **数据管道** | 内存映射文件 | 预分词 `.pt` 张量 + 异步 DataLoader |
| **编译** | `torch.compile` | `torch.compile` |
| **范围** | 完整的 GPT-2 复制 + 微调 | 仅训练流程（无微调） |
| **重点** | 复现 GPT-2 结果 | 展示完整流程：数据 → 分词器 → 模型 |
| **HuggingFace 集成** | 最小化 | 原生——保存为 `AutoModelForCausalLM` |

**关键区别**：nanoGPT 复制了 GPT-2 的精确架构，并能复现已发表的结果。llmTrain 采用了 **更现代的架构**（更接近 LLaMA 风格），并增加了 nanoGPT 所跳过的完整 **分词器训练阶段**。它较少关注基准测试，更注重展示端到端的完整流程。
