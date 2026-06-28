---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳稀疏注意力仓库排名
translated: true
type: note
---

以下是值得你花时间研究的仓库，按理解机制的信噪比排序：

## 原始/权威实现

**[openai/sparse_attention](https://github.com/openai/sparse_attention)** — Child 等人的官方参考实现。代码量小、可读性强。`attention.py` 中直接包含了 stride 和 fixed 模式。这是主要来源——优先阅读。注意它是 TF1 时代的代码，无法直接运行，但模式逻辑才是关键。

## 核心实现（真正落地的部分）

**[openai/triton](https://github.com/openai/triton)** — `python/tutorials/06-fused-attention.py` 教程是 Triton 中关于 block-sparse / fused attention 的权威讲解。从这里开始，“融合块稀疏 GPU 内核”就不再只是概念，而是你可以修改的代码。与你对 CUDA / 推理优化的兴趣直接相关。

**[Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)** — 它本身并非稀疏注意力，但 FlashAttention 基于 IO 感知分块（IO-aware tiling）的思想，取代了 Sparse Transformer 论文中“重新计算以节省内存”的技巧。阅读 `flash_attn/flash_attn_triton.py` 可以看到 Child 等人当年试图实现的现代版本。这是重要的演进脉络。

## 后续发展的脉络

**[lucidrains 仓库]** — Phil Wang 用干净、简洁的 PyTorch 重新实现了几乎所有注意力变体：

- [sparse-attention](https://github.com/lucidrains/sinkhorn-transformer) 以及 routing / reformer 相关实现
- [routing-transformer](https://github.com/lucidrains/routing-transformer) — 基于内容的聚类分支
- [reformer-pytorch](https://github.com/lucidrains/reformer-pytorch) — LSH 分桶分支

这些是并排观察“内容无关 vs 基于内容”分支的最佳方式，每份代码约 200 行，无基础设施依赖。

**[allenai/longformer](https://github.com/allenai/longformer)** 和 **[google-research/bigbird](https://github.com/google-research/bigbird)** — 固定模式注意力（局部 + 全局 + 随机）的直接泛化。BigBird 的 `bigbird/core/attention.py` 展示了固定模式是如何组合的。

## 针对你的工作流的建议

鉴于你喜欢通过动手构建来学习：直接跳到 **Triton 的 fused-attention 教程** 和 **lucidrains 的最小化重新实现**。将两者克隆下来，在你的 4070 上运行，然后把上面提到的 `strided_mask` 草图移植成一个可工作的 block-sparse 注意力层。这是一个紧凑的下午项目，学到的比阅读全部六篇论文还多。

想要一个最小的 nanoGPT 风格训练脚本，将 block-sparse 注意力替换进去，以便在你的硬件上与 dense 注意力进行基准测试吗？
