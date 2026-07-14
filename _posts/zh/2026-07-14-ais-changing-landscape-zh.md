---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI的变革格局
translated: true
type: note
---

问题：AI技术的长期发展趋势是什么——哪些是结构性的变化，哪些是不变的？

答案：

**不变项（不会改变）：**

1. **目标函数。** 下一个词元的交叉熵损失加上梯度下降仍然是所有技术的基础——包括推理模型、智能体、RLHF/RLVR。没有人能替代这一基础。RL后训练只是通过不同的损失信号（奖励而非负对数似然）重新塑造同一个自回归分布。

2. **苦涩教训依然成立，但资源分配方式已经改变。** 计算能力加上通用方法优于手工设计的先验知识，这一原则仍然正确。变化在于，计算能力现在被分配到了三个方向而非一个：预训练计算、后训练/强化学习计算，以及测试时计算。预训练缩放、后训练缩放和测试时缩放共同反映了该领域如何通过技术演进，在日益复杂的用例中利用额外计算。幂律形态是不变的，但计算资源的投入方向是变化的。

3. **Transformer架构核心不变。** 注意力机制与前馈网络模块，无论是稠密还是MoE（混合专家模型），仍然是基础。MLA/GQA是对同一骨架的压缩技巧，而非替代方案。

**实际正在变化的方面：**

1. **预训练缩放正遭遇数据瓶颈，而非数学极限。** Epoch AI预测，在当前训练速率下，经过质量筛选的公开文本存量将在2026至2032年间被完全利用，头部实验室已面临独特词元预算的约束。Muennighoff等人的研究表明，重复词元并非线性稀释——其价值随重复次数呈指数级衰减，且具有可学习的半衰期。这就是为什么"只要增加更多互联网文本"在2020-2023年间曾是免费午餐，如今却已不再。

2. **计算资源从训练阶段转移到测试阶段。** 像o1、o3、DeepSeek-R1和Gemini Flash Thinking这样的模型在推理时使用思维链——在回答前思考更长时间——将认知工作分配到推理步骤中，而非全部编码到训练时的权重里。这是过去18个月中最大的架构变革。它直接利好你的硬件条件——一个较小但训练良好的模型加上更多的推理时搜索，能够击败一个你训练不起的更大稠密模型。

3. **后训练现在遵循自身的缩放定律。** 在RL后训练过程中，测试损失、计算量和数据之间的关系遵循可预测的幂律，适用于基础模型和指令微调模型——但存在潜在的饱和趋势：更大的模型学习效率更高，但随着规模增大，收益递减。RLVR（可验证奖励——数学、代码、单元测试）正成为主导杠杆，正是因为原始文本数据正在枯竭，而来自可执行/可验证任务的奖励信号却不会。

4. **子缩放/密度效应真实存在。** 近期对400多个模型的研究发现，随着数据集变得非常大，性能提升的减速速度超过了标准缩放定律的预测——每个新样本的边际独特性随数据密度下降，导致冗余和递减收益相互叠加。这就是为什么一年后Falcon 180B输给了Llama 3 8B——架构/数据质量/后训练如今胜过原始参数数量。

5. **稀疏性（MoE）是"计算能力受限但你需要更多容量"的主流答案。** 仅激活部分参数的推理方式是DeepSeek、Kimi以及大多数2026年前沿模型默认采用MoE而非稠密架构的原因。这正是你已经在构建的方向。

**对你的构建的总结**：在4070上从头训练一个更大的稠密模型从来都不是可行方案，现在对任何人来说都不是（即使实验室也受限于数据）。前沿已转向：小巧高效的基础模型 → 用于容量-算力比的MoE → 用于能力提升的RLVR/测试时计算，无需更多预训练词元。你的nanoGPT-MoE计划与当前领域实际瓶颈所在一致，而非2022年的状况。

参考文献：
- [AI Scaling Laws Guide Billions in Compute Spend: Weng Reveals the Cracks](https://www.techtimes.com/articles/319204/20260627/ai-scaling-laws-guide-billions-compute-spend-weng-reveals-cracks.htm)
- [LLM Scaling Laws: Analysis from AI Researchers](https://aimultiple.com/llm-scaling-laws)
- [AI Scaling Laws Are Breaking Down: What It Means for AI Builders](https://www.mindstudio.ai/blog/ai-scaling-laws-breaking-down-what-it-means-for-builders)
- [LLM Scaling Laws Explained: Will Bigger AI Models Always Win? (2026)](https://www.buildfastwithai.com/blogs/llm-scaling-laws-explained)
- [How Scaling Laws Drive Smarter, More Powerful AI — NVIDIA Blog](https://blogs.nvidia.com/blog/ai-scaling-laws/)