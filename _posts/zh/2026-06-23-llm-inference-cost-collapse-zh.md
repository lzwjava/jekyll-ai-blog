---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型推理成本骤降
translated: true
type: note
---

**问题：** 当前GPT-4级别大语言模型推理的成本是多少？过去两年间成本下降了多少？

**答案：** 数据是具体的，成本崩塌是真实的。以下是完整图景：

---

## 成本崩塌数据一览

GPT-4同等性能的推理成本现为 **每百万token 0.40美元**，而2022年底为 **每百万token 20美元**。这意味着约3年内实现了 **50倍下降**。推理成本正以每年约10倍的速度下降——比个人电脑计算或互联网泡沫时代的带宽增长更快。

---

## 当前定价层级（2026年6月）

已形成三个清晰的层级：

| 层级 | 模型 | 输出成本 |
| ------ | ------ | ---------- |
| 高端 | Claude Opus 4.6, GPT-5 Pro | 每百万输出token 14–168美元 |
| 中端 | Claude Sonnet 4.6, GPT-5.4, Grok 4 | 每百万输出token 3–15美元 |
| 经济型 | DeepSeek V3.2, Gemini Flash, GPT nano | 每百万输出token 0.40–3美元 |

**对你最相关的数据：**

DeepSeek R1（每百万token输入/输出成本为0.55美元/2.19美元）的推理成本约为o3（每百万输出token 60美元）的 **1/27**。对于大多数生产工作负载，Claude Sonnet 4.6（3美元/15美元）或GPT-5.4（2.50美元/15美元）能实现最佳平衡。DeepSeek V3.2是最便宜的前沿级选项，成本为 **每百万token输入/输出0.14美元/0.28美元**。

---

## 成本崩塌的驱动因素

主要驱动因素：DeepSeek以比现有厂商低90%的定价颠覆了市场。云端H100价格在从2023年峰值下跌64–75%后，稳定在每小时2.85–3.50美元。量化技术使运营成本降低60–70%。推测解码将延迟缩短2–3倍。

在模型架构方面：得益于改进的训练技术，模型在保持性能的同时变得更小——一个130亿参数的模型现在能以显著更小的推理占用达到GPT-3 MMLU分数的95%。

---

## 对你规模的实用影响

按每月约10亿token计算，以下是这些数据对你的意义：

| 模型 | 输入（10亿token） | 输出（假设2亿token） |
| ------- | ------------------- | ---------------------- |
| DeepSeek V3.2 | 140美元 | 56美元 |
| Claude Sonnet 4.6 | 3,000美元 | 3,000美元 |
| Claude Opus 4.6 | 15,000美元 | 15,000美元 |

MiMo免费额度（46亿token）根据对比的模型不同，实际价值为 **644–46,000美元**。

一个值得注意的优化：在超过1000万次请求时，将80%路由到廉价模型、20%路由到前沿模型，相比全部路由到前沿模型可降低60–70%的成本。Anthropic还提供激进的提示缓存折扣，缓存部分最高可享90%优惠。

趋势很明确——再过两年，前沿级能力的每百万token成本很可能从0.40美元降至0.04美元。对于智能体工作负载，瓶颈正从成本转向 **延迟和上下文窗口**。

**参考资料：**

- [推理单元经济学 — Introl博客](https://introl.com/blog/inference-unit-economics-true-cost-per-million-tokens-guide)
- [2026年LLM API定价 — CloudZero](https://www.cloudzero.com/blog/llm-api-pricing-comparison/)
- [LLM定价对比 — IntuitionLabs](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)
