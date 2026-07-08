---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据清洗的分岔
translated: true
type: note
---

**问题：** 当前 IT 行业中，“数据清洗”作为一项工作/角色处于什么状态？

**回答：**

真实情况是两极化，而非简单的“消亡”或“增长”故事：

**1. 纯数据清洗作为独立职位正在被自动化淘汰。** Research.com 2026 年自动化韧性分析对此直言不讳：数据清洗、基础报表等技术角色正在快速自动化，需求萎缩。同样，针对初级数据科学家的作品集建议也已转变——在 ChatGPT 和 AI 工具涌入市场之前，拥有一个包含大量展示数据清洗和数据处理技能项目的作品集非常重要；但如今，这些基础步骤通常由 AI 工具完成。如果某人的全部工作描述就是“编写 pandas 脚本来对 CSV 进行去重/插补/标准化”，那么这个岗位正在被压缩成一次 LLM 调用加上一个审核步骤。

**2. 但数据清洗作为嵌入更高价值角色中的 *功能* 并未缩减——它反而是瓶颈。** 一篇 2026 年的 Medium 文章精准地将其定位为对立面：在 2026 年，多智能体系统和领域特定模型的时代，“垃圾”不仅仅是 CSV 中的缺失值——它是语义漂移、上下文噪声；为了让数据能被智能体通过 MCP 使用，数据需要是原子化的（可独立理解，而非埋藏在 40 页 PDF 中）、新鲜的、且是可归因的（系统是否知道决策原因，还是从遗留电子表格中猜测）。文章的核心论点——你的 AI 并非因模型愚蠢而生成幻觉，而是因数据一团糟——正是“以数据为中心 AI”的论点：模型的实际架构远不如你投喂的燃料质量重要。

**3. 这直接映射到你正在做的事情（为 DeepSeek v4 MoE / nanochat 规模训练进行数据集工程）。** 同一篇文章的实际启示与你的 RLHF/GRPO 工作相关：2026 年最成功的 AI 团队正在增加数据整理过程中的人工监督，使用“银数据”——由模型生成并经人工精炼的数据——来训练更小、更快的“铜模型”；而技巧是：不要只让人工标注数据，还要让他们解释标签为何正确，因为这种推理数据对于现代推理模型来说是黄金。文章还明确警告你的 MoE/合成数据流水线不要陷入自我强化：在没有真实锚点的情况下训练于模型生成的数据会面临模型崩溃风险——AI 放大自身错误，直到变成数字回音室；对边缘情况使用合成数据，但保持锚点数据真实。

**4. 劳动力市场分析印证了这种分化。** 一篇 2026 年职业文章引用的麦肯锡数据：66% 的美国公司表示 AI 将在未来三年内对其成功至关重要，但超过 50% 的公司难以招聘到合适人才——短缺的是能够判断数据质量和上下文的人，而非会运行 `.dropna()` 的人。同一来源：AI 可以在几秒钟内清理大型数据集、分组记录并标记异常值——这些任务过去需要数小时——从而解放分析师去做更高价值的规划和咨询工作。

**对你咨询业务角度的总结：** 不要将“数据清洗”定位为一项服务线——而是将 **“训练数据流水线设计 + 带推理注释的数据整理 + 抗崩溃合成数据策略”** 定位为服务线。这才是 Tinker 级别的护城河：客户不需要有人去重行，他们需要有人能构建银→铜蒸馏流水线，判断哪些数据足够原子化、新鲜、可归因以放入 RAG 或微调语料库，并防止他们的内部合成数据循环崩溃。这正是你已经在用 nanochat/DeepSeek v4 MoE 构建的自然延伸，而且对粤港澳大湾区/香港客户来说，这是一个比“我们帮你清洗数据”高得多的定价诉求。

**参考文献：**

- [The Dirty Secret of AI in 2026: Data Cleaning Job is still a priority](https://medium.com/@ujjwalgupta893/the-dirty-secret-of-ai-in-2026-data-cleaning-job-is-still-a-priority-ecacf4e05dff)
- [2026 Data Analytics Careers Most Resilient to Automation](https://research.com/online-degrees/data-analytics/data-analytics-careers-most-resilient-to-automation)
- [Why AI Data Analysts Are in Massive Demand in 2026](https://workforceinstitute.io/generative-ai/why-ai-data-analysts-are-in-massive-demand-2026)
- [Data Science in 2026: Is It Still Worth It?](https://towardsdatascience.com/data-science-in-2026-is-it-still-worth-it/)
