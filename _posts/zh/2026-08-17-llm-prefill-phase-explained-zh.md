---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM预填充阶段解析
translated: true
type: note
---

问题：在LLM推理中，prefill（预填充）是如何工作的？

答案：

LLM推理分为两个不同的阶段：**prefill**（预填充）和**decode**（解码）。Prefill是第一阶段，模型在此阶段一次性处理整个输入提示，然后才开始生成输出token。

**Prefill期间发生了什么**

1. **Tokenization（分词）**：将输入提示转换为一系列token ID。
2. **并行前向传播**：所有输入token同时通过模型的所有层，完成一次前向传播。由于整个提示已知，这可以作为一个大型矩阵乘法来计算，而不是逐个token进行。
3. **KV缓存构建**：对于每个注意力层，模型计算并存储每个输入token的key（K）和value（V）向量。这些被缓存在内存中（即“KV缓存”），以便后续无需重新计算。
4. **第一个输出token**：在prefill结束时，模型生成词汇表上关于*下一个*token的概率分布，并采样/选择第一个生成的token。

**为什么它要与decode分开**

- **计算模式**：Prefill高度并行且受计算限制（以矩阵乘法为主），因为所有token一起处理。相比之下，decode一次只生成一个token，重用prefill中缓存的K/V，仅计算最新token的K/V。Decode受内存带宽限制而非计算限制。
- **延迟特征**：Prefill决定了“首个token生成时间”（TTFT）。提示越长，prefill时间越长，因为工作量随输入长度增加。Decode决定了生成过程中的每token延迟（“每个输出token的时间”）。
- **硬件利用率**：Prefill通常能高效利用GPU（大规模批处理矩阵乘法），而decode每一步效率较低，因为它一次只计算一个新token——这就是为什么存在连续批处理、推测性解码和分块prefill等技术，旨在提高decode期间的GPU利用率，或在多个请求之间交错执行prefill和decode工作。

**一个简单的类比**：prefill就像在回答前先阅读并完全理解问题——你一次性处理所有内容并建立上下文（KV缓存）。Decode则像逐词说出答案，每个新词只依赖于已阅读和说出的内容，因此你重用已存储的上下文，而不是每次重新阅读整个问题。

**在服务系统中**：许多生产推理引擎（例如vLLM、TensorRT-LLM、Hugging Face TGI）会明确以不同方式优化prefill和decode，有些还使用“分块prefill”技术，将大型prefill工作负载拆分成小块，与其他请求持续进行的decode步骤交错执行，从而提高整体吞吐量并降低尾延迟。

参考文献：
- [Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM论文)](https://arxiv.org/abs/2309.06180)
- [How continuous batching enables 23x throughput in LLM inference](https://www.anyscale.com/blog/continuous-batching-llm-inference)
- [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/)