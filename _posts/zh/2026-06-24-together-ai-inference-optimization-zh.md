---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Together AI 推理优化
translated: true
type: note
---

**问题：** Tri Dao 在 Together AI 的工作中，如何优化推理？

**回答：**

Tri Dao 是 Together AI 的联合创始人兼首席科学家，同时也是普林斯顿大学的助理教授。他的研究处于机器学习与系统交叉领域，专注于硬件感知算法和序列模型。

以下是他在 Together AI 实际从事的推理优化工作：

---

## 1. FlashAttention 系列（核心工作）

整个 FlashAttention 系列是他的主要贡献 —— 如今已成为几乎所有严肃推理栈的支柱。

**核心洞察：** 标准注意力从 HBM（慢）读取 Q、K、V，计算注意力分数，写回 HBM，再读取进行 softmax —— 这造成了巨大的内存带宽浪费。FA 将计算平铺为 SRAM 驻留的块，将整个 QK^T → softmax → V 矩阵乘法融合为单个内核 pass，将 HBM 往返次数从 O(N²) 降至 O(N)。

**FlashAttention-2：** 使用 NVIDIA 的 CUTLASS 3.x 和 CuTe 原语从头重写。比 FA1 快约 2 倍，在 A100（FP16/BF16）上可达 230 TFLOPs/s，端到端 GPT 训练模型 FLOPs 利用率达 72%。

**FlashAttention-3（H100 专用）：** FA2 在 H100 上仅达到理论最大 FLOPs 的 35%。FA3 利用 Hopper 特定的异步指令——WGMMA（warp 组矩阵乘法累加）和 TMA（张量内存加速器）——来重叠操作。从约 350 TFLOPS（FA2 FP16 前向）提升至约 540-570 TFLOPS。关键技术是 **warp 专化**：独立的生产者 warp 发起 TMA 加载，而消费者 warp 运行 WGMMA，将内存延迟隐藏在计算之后。

**FlashAttention-4（Blackwell）：** 在 Blackwell 上，MMA 累加器驻留在 TMEM（而非 Hopper 的寄存器中），这使得在 CUDA 核心处理逐元素工作（softmax、dS）时，可以实际保持多个 MMA 在飞。关键的后向 pass 重叠：在计算 tile j 的 softmax 时，tile j-1 的 dK 和 dQ MMA 已经发出。

---

## 2. Together Kernel 集合

Together AI 基础设施的核心是 Together Kernel 集合——被描述为“在首席科学家 Tri Dao 领导下实现的人工智能系统优化突破”。它提供比超大规模解决方案快 2-3 倍的推理速度。该集合很可能将 FA、自定义解码内核和 MoE 路由内核整合在一个框架下。

---

## 3. 三种推理模式（他的框架）

Tri Dao 识别出三种不同的推理优化目标：
- **聊天机器人工作负载** —— 足够快以感觉响应迅速，但非即时，保持自然的用户体验
- **低延迟超快速推理** —— 用于编码助手（如 Claude Code）或智能体任务，用户愿意支付额外费用以保持流畅
- **最大吞吐量 / 大批量** —— 合成数据生成和强化学习训练展开（采样多条轨迹）

每种模式需要不同的内核/调度策略——而非一刀切。

---

## 4. 混合 Mamba-Transformer + Marconi 前缀缓存

混合 Mamba-Transformer 模型现在已匹配或超越领先的开放模型，同时提供更快的推理和百万 token 上下文。Mamba SSM 组件在解码过程中减少了长上下文的二次 KV 缓存成本。

根据他的出版物页面：**Marconi: Prefix Caching for the Era of Hybrid LLMs** 和 **Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining** 是他团队近期的论文——两者都直接针对推理吞吐量。考虑到 DeepSeek 风格的 MoE 部署，专家激活论文尤其相关。

---

## 简要堆栈

| 层级 | 他的工作 |
|---|---|
| 注意力内核 | FlashAttention 1/2/3/4 — SRAM 平铺、IO 感知、Hopper/Blackwell 异步 |
| 架构 | Mamba/SSM 混合以消除二次 KV 缓存增长 |
| MoE | 机会性专家激活以加快解码 |
| KV 缓存 | 用于混合 LLM 的 Marconi 前缀缓存 |
| 系统 | Together Kernel 集合，面向三种推理模式 |

吞吐量数字对你实际很重要：如果你在 MI300X 上执行强化学习展开或合成数据生成，FA3/FA4 的等价实现（flash-attn 的 ROCm 移植版存在于 `Dao-AILab/flash-attention`）值得尝试——它们在注意力层上决定了 HBM 利用率是 35% 还是 75%+。

**参考文献：**

- [FlashAttention-3 blog](https://tridao.me/blog/2024/flash3/)
- [FlashAttention-4 blog](https://tridao.me/blog/2026/flash4/)
- [Together AI Series B announcement](https://www.prnewswire.com/news-releases/together-ai-raises-305m-series-b-to-scale-ai-acceleration-cloud-for-open-source-and-enterprise-ai-302380967.html)
- [Tri Dao publications](https://tridao.me/publications/)
- [Three inference regimes (X thread)](https://x.com/elliotarledge/status/1970417395476111809)