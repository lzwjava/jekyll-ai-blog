---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大型语言模型中的稀疏注意力机制解析
translated: true
type: note
---

**问题：** 什么是 LLM 中的 Sparse Attention，它是如何工作的？

**回答：**

在标准 transformer 中，每个 token 都会关注其他所有 token —— 这被称为 *全注意*（或 *密集注意*）。对于长度为 N 的序列，意味着 N² 个注意力对，在长上下文中计算量极其巨大。Sparse Attention 的思想是只计算其中 *一部分* 注意力对 —— 让每个 token 只关注精心选择的少数几个，而不是全部。

下面这张图展示了这种对比：关键洞察在于，大多数 token 并不需要查看所有其他 token 就能完成其任务 —— 附近的词和少数几个全局重要位置通常就足够了。Sparse Attention 通过限制注意力模式来利用这一点。

**实践中用到的主要模式：**

**局部 / 滑动窗口（Local / Sliding Window）** —— 每个 token 只关注一个固定大小的邻居窗口（例如 ±128 个 token）。这以 O(N·w) 的代价捕获局部语法和上下文。用于 Longformer。

**步长 / 扩张（Strided / Dilated）** —— token 关注邻居 *以及* 每隔 k 个位置的更远 token。这相当于在局部注意力之上叠加了一层粗略的“全局扫描”。

**全局 token（Global Tokens）** —— 一小部分特殊 token（如 `[CLS]` 或任务相关词）会关注 *所有* 内容，并且所有内容也会关注它们。这为模型提供了一种聚合长距离信息的方式，而无需每对 token 都建立连接。同样用于 Longformer 和 BigBird。

**随机（Random）** —— 每个 token 关注其他 token 的一个随机子集。理论上，与上述模式结合使用时，足以实现全局混合。

**学习型 / 动态（Learned / Dynamic）** —— 模型学习 *哪些* 位置需要被关注，而不是使用固定模式。用于 Reformer（局部敏感哈希）和 Routing Transformers。

**为什么重要：**

全注意在内存和计算上均为 O(N²)。对于一个 10 万 token 的上下文，那就是 100 亿个注意力对 —— 在现有硬件上无法实现。Sparse Attention 将其降低到大约 O(N·k)，其中 k ≪ N，从而实现了长上下文模型。这对于像 Claude 的扩展上下文窗口这样的系统至关重要，不过现代方法往往将稀疏模式与其他技巧（FlashAttention、Ring Attention 等）结合使用。

**权衡：** 你可能会错过那些不在被关注位置上的长距离依赖 —— 这就是为什么混合模式（局部 + 全局 token + 随机）往往优于任何单一模式。

---

**参考文献：**
- [Longformer: The Long-Document Transformer (Beltagy et al., 2020)](https://arxiv.org/abs/2004.05150)
- [BigBird: Transformers for Longer Sequences (Zaheer et al., 2020)](https://arxiv.org/abs/2007.14062)
- [Generating Long Sequences with Sparse Transformers (Child et al., 2019)](https://arxiv.org/abs/1904.10509)
- [Reformer: The Efficient Transformer (Kitaev et al., 2020)](https://arxiv.org/abs/2001.04451)