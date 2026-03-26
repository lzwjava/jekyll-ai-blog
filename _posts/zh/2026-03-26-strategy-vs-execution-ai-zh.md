---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 人工智能开发中的策略与执行
translated: true
type: note
---

**Question:** 为什么大型企业中有很多自称拥有 strategic insights 但在实际 coding 或 AI practice 中毫无作为的人——甚至像李开复这样擅长 strategy 和叙事的人物，在经营自己的 AI startup (01.ai) 时，仍然落后于 Kimi 和 MiniMax 等竞争对手？

---

**Answer:**

这是一个非常敏锐的观察，直接切中了这种已被广泛记录的现象的核心。让我们系统地分析一下。

---

## 1. 大公司内部的“策略层”问题

大型组织在结构上滋生了一群人，他们的全部价值在于“叙事和定位”（narrative and positioning），而非执行。这主要由以下几个原因造成：

**Incentive misalignment（激励错位）。** 在大公司，visibility（可见度）等于晋升。撰写关于“AI strategy”的 PPT 并向 VP 汇报能获得认可；而埋头处理 RLHF pipeline 或调试 CUDA memory 问题则不会。奖励机制惩罚隐形的 engineering，而奖励显性的 storytelling。

**“Visibility mirage”（可见性幻象）。** 研究发现，81% 的业务领导者对自己在 AI execution 方面的监管充满信心，但 75% 的从业者认为领导层低估了 AI execution 的实际难度。结果是，战略决策是基于一个在现实中并不存在的乐观版本做出的。

**Abstraction is safe（抽象是安全的）。** 在高层次上谈论 NVIDIA、GPU compute 趋势或 LLM scaling laws 很容易说得正确。这不需要承担实际的 accountability。如果“strategy”被证明是错的，没人能责怪你——那只是一个“vision”。

**规模产生的 specialization silos（专业化孤岛）。** 在一家拥有 5 万人的公司里，一个人完全可以担任多年的“Chief AI Strategy Officer”，即便他从未训练过模型、写过 transformer attention block，甚至没跑过任何 fine-tuning 任务。组织足够大，足以藏下他们。

---

## 2. 为什么像李开复这样的聪明人在 Execution 中也会挣扎

李开复在宏观分析方面确实才华横溢。他在 2018 年出版的《AI Superpowers》一书对中国 AI 的轨迹具有预见性。他曾是 Microsoft Research Asia 的创始院长，并担任过 Google China 总裁。他的资历是真实的。

但创办 01.ai 揭示了 strategic insight 与竞争性 product execution 之间的根本鸿沟：

**01.ai 严重依赖外部基础。** 他的公司 01.ai 使用 Meta 的 LLaMA 模型构建系统，其团队认为这减少了“从头开始构建所需的努力”。这本身并无坏处，但这意味着 01.ai 在设计上就是一个 fast-follower，而不是原创能力的构建者。

**Consumer traction（消费者吸引力）严重滞后。** 01.ai 的聊天机器人“万知”在 [2024年] 9 月的访问量仅为 10 万次，而竞争对手 Baidu 的 ERNIE Bot 和 Moonshot 的 Kimi 访问量超过 2000 万次。Kimi 特别建立了一种以产品为核心、由用户反馈驱动的文化，这是 01.ai 无法企及的。

**被迫退出 frontier model 训练。** 在 [2025年] 1 月，李开复宣布 01.ai 将放弃预训练万亿参数模型，转而优先考虑更小、更快且具备商业可行性的系统。这是一个重大的战略撤退——本质上承认了 DeepSeek、Alibaba 和 ByteDance 拥有更强大的 raw compute 和研究深度。

**李开复自己也预测了整合。** 李开复预测中国 AI 行业将围绕三个主要的 AI model 开发商进行整合：DeepSeek、Alibaba 和 ByteDance，其中 DeepSeek 目前在势头上处于领先地位。值得注意的是，01.ai 并不在这个名单中。

---

## 3. 为什么“Insight”无法转化为 Execution

核心点在于：**Strategic pattern recognition（战略模式识别）与 deep technical execution 是完全不同的认知和组织肌肉。**

了解“中国拥有强大的 AI 工程师、低廉的劳动力成本和激进的资本”（经典的李开复论点）是有价值的。但实际组建一支能够完成以下任务的团队则完全不同：
- 设计新颖的模型架构（如 DeepSeek 的 MoE 创新）
- 优化 inference 效率
- 通过快速 iteration loops 构建具有粘性的 consumer product
- 在 data flywheel 效应上进行竞争

这需要一种完全不同的、带有强迫症色彩的底层 execution 文化。

李开复自己曾警告说，“许多 LLM 公司是由只关心做出优秀模型的 researcher 经营的”——然而讽刺的是，跑赢他的公司（如 DeepSeek）恰恰是那些技术控的 builder，而不是 strategy-first 的领导者。

Kimi (Moonshot AI) 和 MiniMax 是由年轻且深谙技术的团队创办的，他们以 startup 的速度进行产品 iterate。Kimi 团队被称为“最懂 AI 的”，展现了对产品磨合的极致追求。这种文化很难由一个主要技能在于 capital allocation、董事会关系和媒体 narrative 的人去制造。

---

## 4. 更广泛的模式：为什么这是结构性的

这种脱节被称为“AI leadership gap”——即高管的乐观情绪与将 AI 投资转化为可衡量业务成果所需的实际理解之间的脱节。研究发现，58% 的组织对 AI 倡议没有明确的 ownership，75% 的组织缺乏全面的治理框架。

AI pilots 失败不是因为模型的局限性，而是因为 integration、治理和 execution 的差距压倒了最初的收益。

残酷的事实是：**strategy 是一种商品（commodity），而 execution 是稀缺品。** 任何人都能阅读 NVIDIA 的财报并推断出 GPU 需求将爆炸式增长。但几乎没有人能组建一支团队，以 1/10 的成本交付出优于 OpenAI 的模型（DeepSeek 做到了）。市场最终会为此准确定价——这就是为什么 01.ai 正在淡出，而 DeepSeek 主导了 2025 年的叙事。

---

## Summary

| 特质 | Strategy-Class Leaders | Execution-Class Builders |
|---|---|---|
| 核心技能 | Narrative, positioning | Coding, model training, product |
| 风险暴露 | 低（想法是不可证伪的） | 高（代码要么能跑，要么不能） |
| 大公司价值 | 高（显眼，易晋升） | 往往是隐形的/被低估的 |
| 创业成功率 | 较难——没有组织可以躲藏 | 基础更稳固 |
| 案例 | 许多 SVP, 部分 VC, 早期的 01.ai | DeepSeek, Kimi, 早期的 OpenAI |

你所识别出的模式是真实存在且有据可查的。AI 时代对仅凭 strategy 的玩家来说尤其残酷，因为产品交付的是 code，而不是 slide decks——而且市场可以客观地对不同模型进行 benchmark。

---

**References:**

- [Kai-Fu Lee / 01.AI — Cornell Emerging Markets](https://business.cornell.edu/hub/2024/12/13/chinas-domestic-ai-competition-heats-up/)
- [01.AI vs Kimi usage data — Analytics India Magazine](https://analyticsindiamag.com/ai-news-updates/kai-fu-lees-ai-startups-01-ai-claims-to-have-surpassed-gpt-4o/)
- [01.AI abandons pre-training — TechNode](https://technode.com/2025/03/21/01-ai-founder-kai-fu-lee-predicts-the-endgame-of-chinas-ai-models-names-deepseek-as-frontrunner/)
- [AI Leadership Gap research — Innovation Visual](https://www.innovationvisual.com/knowledge-hub/knowledge/the-ai-leadership-gap)
- [Kai-Fu Lee warns of VC reckoning — Fortune](https://fortune.com/asia/2024/03/27/china-ai-kai-fu-lee-warns-investor-reckoning-unprofitable-ai-companies/)
- [China AI 2024 Year in Review — Recode China AI](https://recodechinaai.substack.com/p/top-10-chinas-ai-stories-in-2024)