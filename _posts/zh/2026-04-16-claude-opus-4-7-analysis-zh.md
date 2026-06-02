---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Opus 4.7 分析与比较
translated: true
type: note
---

**提问：** Opus 4.7 表现如何？它优秀吗？用户反馈怎样？与 Opus 4.6 有何不同？

**回答：**

Claude Opus 4.7 于今日（2026年4月16日）刚刚发布，相比 Opus 4.6 在高级软件工程和复杂编程任务方面表现出显著提升。

## 总体评估

Opus 4.7 在高级软件工程领域相比 Opus 4.6 有明显进步，尤其是在最困难的任务上。用户反馈称，他们能够放心地将最棘手的编码工作交给 Opus 4.7 处理，包括那些过去需要密切监督的任务。该模型在处理复杂、长期运行的任务时展现出更强的严谨性和一致性。

## 相比 Opus 4.6 的主要改进

**1. 增强的编码能力**
- 多家公司报告编码基准测试成绩显著提升
- 在一项包含 93 个任务的编码基准测试中，Claude Opus 4.7 的解决率比 Opus 4.6 高出 13%，其中包含四项 Opus 4.6 和 Sonnet 4.6 都未能解决的任务
- 更擅长发现和修复错误，代码质量更高，错误更少
- 更能处理多步骤工作流和长期运行的自主任务

**2. 增强的视觉能力**
- 能以更高分辨率处理图像，支持处理长边最大 2,576 像素的图像（约 3.75 百万像素），是之前 Claude 模型的三倍多
- 在测试中视觉识别能力大幅提升（一项基准测试得分 98.5%，而 Opus 4.6 为 54.5%）

**3. 更好的指令遵循能力**
- Opus 4.7 在遵循指令方面有实质性改进
- 更精确地按字面意思理解指令，这意味着为早期模型编写的提示词可能需要调整

**4. 提升的专业输出质量**
- 在完成专业任务时更有品味和创意
- 能生成更高质量的界面、幻灯片和文档
- 设计决策更优，创意选择更强

**5. 增强的金融与知识工作能力**
- 在金融智能体评估中达到领先水平
- Opus 4.7 在包括金融智能体评估和衡量金融与法律领域经济价值知识工作的 GDPval-AA 等多个基准测试中得分高于前代模型

## 用户反馈

早期测试用户反馈非常积极，覆盖多个行业：

- **编码/开发**：Cursor、Replit、Cognition（Devin）等公司报告任务完成率有两位数提升
- **设计**：用户认为它是构建仪表盘和数据丰富界面的最佳模型，其设计品味令人惊喜
- **法律**：在高强度设定下，于 BigLaw Bench 基准测试中达到 90.9% 的准确率
- **企业工作流**：更擅长处理模糊问题、在长时间会话中保持高效，并管理复杂的多步骤任务
- **自主性**：更能独立应对具有挑战性的问题，无需持续监督

## 重要注意事项

**1. 能力不及 Mythos**
尽管 Opus 4.7 有所进步，但其能力仍不及 Claude Mythos Preview（Anthropic 最强大的模型）。由于 Project Glasswing 中概述的安全考虑，Mythos Preview 的发布仍受限制。

**2. 降低的网络能力**
Anthropic 在训练中降低了该模型的网络能力（与 Mythos Preview 相比），并实施了自动检测和阻止表明有禁止或高风险网络安全用途请求的安全措施。

**3. 令牌使用变化**
- 使用更新的分词器，相同输入可能产生 1.0 至 1.35 倍的令牌数
- 在高强度设置下，由于推理量增加，可能产生更多输出令牌

**4. 新的强度级别**
Anthropic 引入了介于“高”和“最高”之间的新“xhigh”强度级别，为用户在推理能力和响应速度之间提供了更多控制选项。

## 定价与可用性

定价与 Opus 4.6 保持一致：输入令牌每百万 5 美元，输出令牌每百万 25 美元。该模型已在所有 Claude 产品、Claude API、Amazon Bedrock、Google Cloud 的 Vertex AI 和 Microsoft Foundry 上提供。

## 总结

Opus 4.7 是一次重大升级，尤其在复杂编码任务、视觉能力和专业工作质量方面表现出色。早期用户的反馈非常积极，许多人称其为“明显的进步”，并注意到在实际应用中有实质性改进。然而，与更强大但受限制的 Mythos Preview 相比，它被定位为更安全、更广泛可用的模型。

**参考文献：**

- [https://www.anthropic.com/news/claude-opus-4-7](https://www.anthropic.com/news/claude-opus-4-7)
- [https://www.investing.com/news/economy-news/anthropic-launches-claude-opus-47-with-enhanced-coding-capabilities-4618554](https://www.investing.com/news/economy-news/anthropic-launches-claude-opus-47-with-enhanced-coding-capabilities-4618554)
- [https://decrypt.co/364483/anthropic-opus-47-full-stack-ai-studio-mythos](https://decrypt.co/364483/anthropic-opus-47-full-stack-ai-studio-mythos)
