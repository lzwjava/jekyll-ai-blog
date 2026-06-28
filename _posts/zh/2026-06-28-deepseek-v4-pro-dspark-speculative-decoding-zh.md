---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V4 Pro DSpark 推测解码
translated: true
type: note
---

**问题：** Hugging Face 上的 `deepseek-ai/DeepSeek-V4-Pro-DSpark` 是什么？

**回答：**

关键在于 `-DSpark` 后缀。DeepSeek-V4-Pro-DSpark 并非新模型，它是在原 DeepSeek-V4-Pro checkpoint 基础上附加了一个推测解码（speculative decoding）模块。名称灵感来源于“DeepSeek + Spark”（推测）。参考实现位于他们的 [DeepSpec](https://github.com/deepseek-ai/DeepSpec) 仓库。

因此，这个仓库 = 基础权重 + 用于**自推测解码**的草稿/预测头（类似于 Medusa/EAGLE 风格的多 token 预测），旨在加速推理而不改变模型质量。草稿模块提出若干未来 token，完整模型通过一次前向传播验证这些 token，接受者被提交——从而将多个顺序解码步骤转化为一个经过验证的批次。这就是该仓库显示额外张量类型（`F8_E8M0`、`I8` 等）的原因——推测模块与主 FP4+FP8 权重一同发布。

**模型本身（DeepSeek-V4 系列）：**

这是 **V4 预览版**——相较于 V3.2 的代际跃升。两个 MoE 变体，均支持 1M token 上下文：

| 模型 | 总参数量 | 激活参数量 | 精度 |
|---|---|---|---|
| V4-Flash | 284B | 13B | FP4+FP8 |
| V4-Pro | 1.6T | 49B | FP4+FP8 |

鉴于你对 MoE/注意力的关注，架构上值得注意的部分如下：

1. **混合注意力 (CSA + HCA)** —— 压缩稀疏注意力（Compressed Sparse Attention）与高度压缩注意力（Heavily Compressed Attention）相结合。在 1M token 上下文下，V4-Pro 仅需 V3.2 单 token 推理 FLOPs 的 27% 和 KV 缓存的 10%。这是 V3.2 的 DSA（DeepSeek 稀疏注意力）的自然演进——他们将注意力预算拆分为两个压缩区间，而非单一区间。10% KV 缓存这一数字是长上下文服务经济性的关键指标。

2. **流形约束超连接 (mHC)** —— 对传统残差连接的增强，旨在提高跨层信号传播的稳定性，同时保持表达力。这可以理解为超连接工作（将单一残差流替换为可学习的多流连接）的约束变体，加上流形约束以保证在 1.6T 规模下的训练稳定性。

3. **Muon 优化器** —— 主训练阶段已从 AdamW 切换至 Muon。Muon 用于更快的收敛和更高的训练稳定性。这与 Kimi/Moonshot 方向一致；值得注意的是 DeepSeek 在万亿参数规模上采用了它。

4. **训练 + 后训练**：在 32T+ token 上预训练，采用两阶段后训练范式——通过 SFT 和 GRPO RL 独立培养领域专家，然后通过在线策略蒸馏统一整合。因此，他们分别训练专家，再通过在线策略蒸馏回单一模型。这是对“合并专家”问题的一种更清晰的解决方案，优于简单的权重平均。

**三种推理模式**（Non-think / Think High / Think Max），其中 Max 需要 ≥384K 上下文窗口及特殊系统提示。在基准测试中，V4-Pro-Max 在 LiveCodeBench（93.5）和 Codeforces rating（3206）上领先，与其他模型（Opus-4.6、GPT-5.4、Gemini-3.1-Pro）互有胜负——在编程方面是最强的开源模型，但在原始知识（SimpleQA）上仍落后于 Gemini。

对你而言：如果本地部署或测试 V4，**DSpark 是你为提升吞吐量所需的仓库**——推测模块让 49B 激活参数 / 1M 上下文的解码在你的硬件预算下变得可承受。推荐采样参数为 `temperature=1.0, top_p=1.0`。

**参考资料：**

- [deepseek-ai/DeepSeek-V4-Pro-DSpark](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark)
- [DeepSeek-V4 Technical Report (arXiv 2606.19348)](https://arxiv.org/abs/2606.19348)
- [DeepSpec repo](https://github.com/deepseek-ai/DeepSpec)