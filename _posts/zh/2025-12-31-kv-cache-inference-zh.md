---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解大语言模型推理中的 KV 缓存
translated: true
type: note
---

Question: Explain the KV cache in detail.

Answer:

# 深入详解 Large Language Models 中的 KV Cache

**KV cache** (Key-Value cache) 是 Transformer 架构 Large Language Models (LLMs) 在 Inference 阶段（特别是像 GPT 这样的 autoregressive decoding 模型）中使用的一种关键优化技术。它通过牺牲一定的内存空间来换取计算效率，显著减少了逐个 Token 生成时的计算冗余，提升了生成速度。

## 背景：Transformers 中的 Self-Attention

在 Transformer 架构中，Self-Attention 机制允许模型衡量序列中不同 Token 的重要性。对于每个 Token，模型会从其 Hidden Representation 中计算出三个向量：

- **Query (Q)**：代表当前 Token 正在“寻找”什么。
- **Key (K)**：代表其他 Token 能“提供”什么。
- **Value (V)**：代表其他 Token 包含的实际信息。

Attention 分数计算公式如下：

\\[
\text{Attention} = \softmax\left(\frac{Q K^T}{\sqrt{d_k}}\right) V
\\]

其中 \\(d_k\\) 是 Key 的维度。

在 Multi-head attention 中，这一过程在多个 Head 上并行执行。

在 **Training** 阶段，整个序列是并行处理的，因此所有的 Q、K、V 都是一次性计算完成的。

在 **Inference** 阶段（文本生成），Token 是以 autoregressive 方式产生的：即一次只生成一个。每一步输入都会增加一个 Token。

## 不使用 KV Cache 的问题

如果没有缓存机制：

- 为了生成下一个 Token，模型必须重新处理整个序列（包括 Prompt + 所有已生成的 Token）。
- 这意味着每次生成都需要**重新计算所有先前 Token** 的 K 和 V。
- Attention 的计算成本随序列长度呈**平方级**增长（总体生成步骤为 O(n²)）。
- 对于长度为 n 的序列，生成第 (n+1) 个 Token 需要对所有 n+1 个 Token 重新计算 Attention。

这会导致极高的延迟，尤其是在处理长上下文或长输出时。

## KV Cache 的工作原理

核心洞察：在 autoregressive 生成过程中，先前 Token 的 K 和 V 向量在生成新 Token 时是**不会改变的**。只有新 Token 的 Query (Q) 需要与所有先前的 K 和 V 进行交互。

KV cache 通过以下方式解决问题：

1. 在 **Prefill Phase**（处理初始 Prompt）期间：
   - 并行计算所有 Prompt Token 的 Q, K, V。
   - 将这些 K 和 V Tensors 存储在 Cache 中。

2. 在 **Decode Phase**（逐一生成新 Token）期间：
   - 对于新生成的 Token：
     - 只计算该 Token 自身的 Q, K 和 V。
     - 从 Cache 中检索所有先前的 K 和 V。
     - 将新的 K 和 V 拼接（Concatenate）到 Cache 中。
     - 使用新的 Q 与完整的（缓存的 + 新的）K 进行 Attention 计算，然后乘以 V。
   - 通过追加新的 K 和 V 来更新 Cache。

这使得 Decoding 阶段的 Attention 计算从平方级降为随序列长度**线性**增长：每个新 Token 增加的是 O(n) 的操作，而不是 O(n²)。

### KV Cache 的维度

通常，Cache 的形状如下：

- K 和 V 分别为：[batch_size, num_heads (或 num_kv_heads), sequence_length, head_dim]。

内存占用随序列长度、Batch size 和模型大小线性增长。对于大模型（如 70B 参数）和长上下文（如 128k Tokens），KV cache 可能会占据大部分 GPU 显存。

## 优点

- **速度**：减少了冗余计算；对于长序列，生成过程从计算密集型（Compute-bound）转变为内存密集型（Memory-bound）。
- **更低延迟**：这对于像 Chatbots 这样的实时应用至关重要。
- **可扩展性**：支持更长的上下文窗口。

## 缺点与优化方向

- **内存瓶颈**：对于极长序列或大 Batch，KV cache 的大小可能会超过模型权重的内存占用。
- 常见的优化方案：
  - **Quantization**：降低 KV cache 的精度（例如降至 INT8 或 FP8）。
  - **PagedAttention**：类似虚拟内存的分页机制，防止内存碎片化（应用于 vLLM）。
  - **Grouped-Query Attention (GQA) 或 Multi-Query Attention (MQA)**：让多个 Head 共享 K/V，以减小 Cache 体积。
  - **Eviction/Compression**：移除不重要的条目（例如 StreamingLLM 保留“Sink”Tokens）。
  - **Offloading**：由于长度极端，将部分缓存移动到 CPU 或硬盘。

在 Hugging Face Transformers 等框架中，生成时默认启用 KV caching（通过 `use_cache=True` 参数）。

KV cache 是实现大规模高效 LLM 推理的核心技术，它将潜在的、无法承受的平方级计算成本转化为可控的线性成本。

References:  

- [KV Caching Explained: Optimizing Transformer Inference Efficiency](https://huggingface.co/blog/not-lain/kv-caching)  
- [Transformers Key-Value Caching Explained](https://neptune.ai/blog/transformers-key-value-caching)  
- [Understanding and Coding the KV Cache in LLMs from Scratch](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)  
- [Mastering LLM Techniques: Inference Optimization (NVIDIA)](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/)  
- [Hugging Face Documentation on KV Cache](https://huggingface.co/docs/transformers/en/kv_cache)