---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 学习复制专家判断
translated: true
type: note
---

**问题：** Thinking Machines Lab 和 Bridgewater 是如何通过 Tinker API 合作的？项目内容、训练方案和结果分别是什么？

**回答：**

这是 2026 年 6 月 30 日由 Sarah Su、Kevin Zhu、Emily Xiao、Rohan Alur（Thinking Machines）和 Daniel Kang（Bridgewater AIA Labs）发表的《学习在金融任务中复制专家判断》工作。这是目前 Tinker 在生产环境中最有力的公开案例研究，且与你第一阶段的咨询论文直接相关。

**问题所在。** 他们评估了模型在六项信息筛选任务上的表现，这些任务来自投资者日常工作流程——例如，给定一篇金融文章，判断其是否与 C 级投资专业人士相关；给定一份央行文件，判断其是否预示未来利率变化方向。难点在于：正确回答往往依赖 Bridgewater 的内部工作流程而非公开网络知识——仅凭任务描述，Gemini、Claude 和 GPT 变体的平均准确率约为 50%。专家编写的提示词（包括一个巧妙的标签重构：相关且有趣/相关但不有趣/不相关）将前沿模型的表现从抛硬币水平提升到 70% 中段，而自动提示优化并未带来进一步增益。即便使用最佳提示词，前沿模型的准确率仍低于投资者信任所需的 80% 阈值。

**模型与平台。** 他们通过 Tinker 对 Qwen3-235B（MoE）进行了微调，Tinker 使用 LoRA 适配器，确保客户数据与客户模型绑定，并开放前向-反向传播、优化器步进、采样和保存状态等基础操作。Tinker 负责基础设施层面，使团队无需直接管理 GPU 集群即可快速迭代。

**训练方案**——这对你来说是最有趣的部分：

该方法结合了专家标注的微调数据与 GRPO、交错批处理（+12.1%）、带非对称裁剪的 CISPO 损失（+10.1%）以及使用动态提升教师模型进行在线策略蒸馏（+3.1%）。在线策略蒸馏中，学生模型从其自身尝试的输出中学习，同时由更强的教师模型进行评分。注意，该方案基本就是 tinker-cookbook 中已有的内容——SFT → 使用 GRPO 系列目标的 RL → 在线策略蒸馏——但有两个非显而易见的技巧（交错批处理和非对称 CISPO 裁剪）发挥了主要作用。仅靠承包商标注是不够的——专家标注才是真正的数据集护城河。

**结果。** 定制模型达到了 84.7%，而最佳专家提示的前沿基线为 78.2%——错误率降低了 29.8%，且运营成本显著降低——每次调用的推理成本便宜 13.8 倍。值得注意的保留意见：这些是公司在内部六项任务评估中自行测量的结果，因此具体数字可能带有营销色彩，但方向是可信的。

**战略框架。** 他们称之为“差异化智能”——针对特定组织需求调整的定制模型超越了前沿模型。Tinker 是正在被验证的商业产品；每个拥有专有专家标注数据的机构都是 Tinker 的潜在客户。

**这对你特别重要的原因：** 这实际上就是你第一阶段计划中写下的剧本——“Tinker 级别技能作为护城河”、高端客户、基于专有判断数据的微调。Bridgewater 的结果就是你可以向大湾区/香港金融客户展示的销售文档：前沿 API + 提示词在部署阈值以下达到上限；专家标注 + 在开源 MoE 上进行 LoRA 微调以 1/14 推理成本突破阈值。可复现的部分（GRPO、在线策略蒸馏、Qwen MoE 上的 LoRA）都在开源的 tinker-cookbook 中——值得在公开数据集上复现一个迷你版本作为作品集。另外注意，cookbook 现在包含了教授 Claude 使用 Tinker API 的 Claude Code 技能（`/plugin marketplace add thinking-machines-lab/tinker-cookbook`），这符合你以智能体为先的工作流程。

**参考资料：**

- [学习在金融任务中复制专家判断——Thinking Machines Lab](https://thinkingmachines.ai/news/learning-to-replicate-expert-judgment-in-financial-tasks/)
- [Bridgewater 测试表明 GPT、Claude 落后于调整后的 Qwen 模型——WinBuzzer](https://winbuzzer.com/2026/07/04/bridgewater-test-says-gpt-claude-lag-tuned-qwen-model-xcxwbn/)
- [TML × Bridgewater 分析——FourWeekMBA](https://fourweekmba.com/ai-thinking-machines-lab-bridgewater-custom-model-beats-frontie/)
- [tinker-cookbook——GitHub](https://github.com/thinking-machines-lab/tinker-cookbook)