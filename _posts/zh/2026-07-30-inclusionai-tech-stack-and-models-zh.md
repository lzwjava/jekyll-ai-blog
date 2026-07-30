---
audio: false
generated: true
image: false
lang: zh
layout: post
title: InclusionAI 技术栈与模型
translated: true
type: note
---

**问题：什么是InclusionAI，以及他们的技术栈/模型阵容是什么？**

**回答：**

**关于他们**

InclusionAI（IAI）由蚂蚁集团创立，团队成员包括前OpenAI、Google和FAIR（Meta AI）的研究人员，定位为一个由所有人构建、服务于所有人的开源AGI平台。它并非初创公司——蚂蚁集团是阿里巴巴关联的金融科技公司（支付宝母公司），因此这是一个资金雄厚的现有企业的AGI实验室，类似于DeepSeek从量化基金中诞生的精神。

关键人员（根据AI Wiki资料，需对组织维基信息保持常规审慎态度）：吴毅（前OpenAI，伯克利博士）、乐振中（CMU毕业，前Google AI）、蔡伟（斯坦福，前Google，曾参与图像搜索/云视觉API工作）、沈春华（h指数130+）、杨明（FAIR创始成员）、郑达（蚂蚁图计算实验室），以及何正宇（佐治亚理工博士，GPU最大流算法）担任蚂蚁集团CTO及AGI项目执行发起人。

**你可能会关注的模型阵容**

1. **Ling系列**——旗舰级Dense/MoE大语言模型。
   - Ling-2.6-1T是一个万亿参数模型，采用"快思考"机制，与长思维链推理模型不同，专注于智能体时代的执行任务：代码编辑、工具调用、复杂指令遵循。它支持262.1k token上下文，最大输出32.8k token，可通过OpenRouter免费API使用，并计划开源。
   - 前代模型Ling-1T曾在2025年末的开源模型汇总中被视为中国地区的重要发布之一。

2. **LLaDA2.0/2.X**——扩散大语言模型，非自回归模型。包含LLaDA2.0-mini（16B）和LLaDA2.0-flash（100B），均为MoE架构，标志着扩散语言模型首次扩展到100B参数规模。LLaDA2.0-flash-CAP通过并行解码达到535 tokens/秒，速度是同类自回归模型的2.1倍。两个规模的权重和训练代码均已在Hugging Face上完全开源。如果你从事推理/服务相关工作，这可能会引起你的兴趣——在100B MoE规模上实现并行解码是一个真正的系统工程成就，而不仅仅是论文成果。

3. **Ming**——基于Ling大语言模型主干构建的多模态理解/生成模型。

4. **ZwZ系列**——2026年ICML的细粒度感知模型，搭配新的感知基准ZoomBench。

5. **Ring-Zero**——研究论文（arXiv，2026年7月14日），在Ling架构上推动零强化学习（基于原始基座模型、无人类标注数据的强化学习）至1T参数规模。论文记录了五种非人为设计的涌现行为：自我验证、并行推理、结构化格式化、拟人叙事和"上下文焦虑"——模型在推理过程中主动管理自身的计算预算。如果你从事强化学习后训练，值得一读——这是关于涌现行为的真实规模定律结果，而非营销噱头。

**你可以实际使用的基础设施**

AReaL（蚂蚁推理强化学习）——面向推理/智能体模型的开源异步强化学习训练系统，与清华大学交叉信息研究院合作开发。它将交互式数据生成与策略更新解耦，使得GPU利用率在推理和训练工作节点间保持连续，避免了标准强化学习流程中的同步停顿瓶颈。考虑到你已经在MI300X集群上进行模型训练，如果你正在构建或调整自己的强化学习循环，这种异步数据生成/策略解耦方案直接相关——它与OpenRLHF/veRL属于同一类问题，但蚂蚁集团强调以连续GPU利用率为核心指标。

此外还有：ABench（内部基准测试套件）和dInfer（为扩散语言模型构建的推理框架，随Ling-1T一起发布）。

**需要明确指出的注意事项（而非隐藏）**：InclusionAI在蚂蚁集团旗下运营，总部位于中国，受中国《国家情报法》（2017年）、《数据安全法》（2021年）和《网络安全法》（2017年）约束——如果你通过其API/OpenRouter端点路由生产流量，而非自托管开源权重，这一点需要关注。

参考文献：

- [InclusionAI GitHub组织](https://github.com/inclusionAI)
- [LLaDA2.X仓库](https://github.com/inclusionAI/LLaDA2.X)
- [Ling-2.6-1T公告](https://phemex.com/news/article/ant-group-unveils-ling261t-a-trillionparameter-ai-model-76554)
- [Interconnects采访蚂蚁Ling及InclusionAI负责人](https://www.interconnects.ai/p/inside-a-chinese-frontier-lab-inclusion)
- [Ring-Zero相关报道](https://www.techtimes.com/articles/320677/20260716/trillion-parameters-no-human-labels-ant-group-documents-five-emergent-ai-behaviors.htm)
- [AI Wiki：InclusionAI](https://aiwiki.ai/wiki/inclusionai)
