---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大型语言模型中的KV缓存
translated: true
type: note
---

问题：在大语言模型（LLM）的语境中，什么是 KV 缓存（键值缓存）？

答案：

KV 缓存（键值缓存）是一种用于基于 Transformer 的语言模型中的优化技术，旨在避免文本生成过程中的冗余计算。

**Transformer 的工作原理（简要说明）：**
在注意力机制中，每个令牌会生成三个向量：**查询（Q）**、**键（K）**和**值（V）**。为了生成每个新令牌，模型需要对*所有先前令牌*计算注意力——这意味着它需要这些令牌的 K 和 V 向量。

**无缓存时的问题：**
如果没有缓存，模型会在*每一个生成步骤*中为每一个先前看到的令牌重新计算 K 和 V 向量——这极其低效。

**KV 缓存的作用：**
它将已处理令牌的 K 和 V 向量存储在内存（RAM 或显存）中。当生成下一个令牌时，模型只需：
1. 仅为*新*令牌计算 K/V
2. 将其**追加**到缓存的 K/V 向量中
3. 使用完整的缓存历史进行注意力计算

这将每一步的计算复杂度从 O(n²) 降低到约 O(n)，从而显著加快推理速度。

**权衡：**

| 优点 | 代价 |
|---|---|
| 令牌生成速度大幅提升 | 高内存占用 |
| 减少冗余计算 | 内存随上下文长度增长 |
| 对长上下文必不可少 | 可能限制 GPU 上的批处理大小 |

**你会在哪些地方遇到它：**
- Anthropic 的**提示缓存**功能——缓存重复使用的系统提示的 KV 状态，从而避免重复调用时的计算成本
- vLLM 的 **PagedAttention**——像操作系统虚拟内存一样管理 KV 缓存内存
- **推测解码**——在草稿模型和目标模型之间共享 KV 缓存

参考资料：
- [Anthropic 提示缓存文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [面向 LLM 服务的高效内存管理与 PagedAttention](https://arxiv.org/abs/2309.06180)
- [图解 Transformer – Jay Alammar](https://jalammar.github.io/illustrated-transformer/)