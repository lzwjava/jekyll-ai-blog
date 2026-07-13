---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计算成本已无关紧要
translated: true
type: note
---

问题：使用 DeepSeek V4 Flash 而非 Sonnet 作为计算后端，重新计算工作室经济学。

答案：

**首先是成本：**

DeepSeek V4 Flash：输入 $0.14/M（缓存未命中），缓存命中输入 $0.028/M，输出 $0.28/M —— 无美国模型外汇或出口管制依赖，MIT 许可权重，100 万上下文。针对代理循环（85% 输入 / 15% 输出 token，70% 缓存命中率）混合计算：

```
DeepSeek V4 Flash 混合成本： $0.094/M  =  0.68 人民币/M token
Sonnet 5 混合成本（先前）：   28.8 人民币/M
                             -> 便宜 42 倍
```

**但这并非免费 —— 存在质量代价。** Flash 在单次编码上与 Sonnet/Opus 层级相当（SWE-bench Verified 79.0% vs 前沿 ~87-95%，LiveCodeBench 91.6%），但在链式多步工具使用和长程代理循环上差距扩大（GDPval-AA 1388 vs Pro 的 1554），并且 Terminal-Bench 2.0 跑分为 56.9% vs Pro 的 67.9% —— 这正是你的工作室完成完整项目构建所依赖的“运行 CLI、迭代、调试、重试”循环。此外，当它不知道答案时，幻觉率为 96%，而 V4 Pro 为 94% —— 它会自信地回答，而不是承认不确定性。请为重试/验证预留预算：

```
考虑代理能力不足的 1.5 倍重试代价后：实际有效成本 1.02 人民币/M
仍比 Sonnet 混合成本便宜 28 倍
```

**这对每月 4 个项目的工作室意味着什么：**

```
使用 Flash 时的 token 销货成本（4 个项目，每个 1400 万 token）：57 人民币（占 10 万收入的 0.057%）
使用 Sonnet 时 token 销货成本已仅为 1,600 人民币（1.6%）
```

诚实的答案：**对你的 headline 利润率几乎无影响，因为计算成本本来就无关紧要。** 从收入的 1.6% 降至 0.06% 并不会改变你的损益表。真正改变的是：

1. **模型路由，而非模型替换。** DeepSeek 自身的指南明确：默认使用 Flash，仅当特定任务类型未通过你的评估时才升级到 Pro（或前沿闭源模型）。对于小程序/网站构建中 80% 的样板代码 —— CRUD 脚手架、表单生成、测试编写、文档、重复性重构 —— 使用 Flash；将 Sonnet/Opus 级别的调用保留给架构决策、棘手的多文件代理调试循环，以及任何面向客户的任务 —— 这类任务中自信但错误的幻觉答案若被发现较晚，代价高昂。

2. **计算成本变得如此低廉，你可以将其花在稳健性上，而不是节省它。** 既然在 Sonnet 价格下销货成本都已微不足道，那么在 Flash 价格下，你可以为每个功能生成 3-5 个候选实现、运行详尽的测试生成流程，并让代理积极重试和自我修正 —— 用 token 换取可靠性，而不是用自己的审查时间。这才是真正的杠杆：不是更便宜的项目，而是在相同项目下，减少人力 QA 负担，因为你可以几乎免费地投入 10 倍的 token 预算进行自我验证。

3. **非成本因素在此比价格更重要。** MIT 许可意味着可自托管（不依赖外部 API 可用性 —— 鉴于 Claude Managed Agents 计费变化以及今年因出口管制/政策事件导致模型访问方式普遍变化，这一点相关），以人民币计价的成本敞口而非美元，并且如果自托管，数据不会离开中国 —— 这对具有数据驻留条款的客户合同是一个真实的考量。

4. **重试代价是一个你应该实测而非假设的实时数字。** 1.5 倍是一个占位符 —— 将你的实际小程序流水线在 Flash 与 Sonnet 上分别运行，记录在你自己的验收测试上的通过/失败情况，并计算真实比率。考虑到利润率（28-42 倍原始成本），Flash 在几乎任何不超过 ~20-30 倍的重试代价下都胜出，而这在小程序构建中占大部分的样板代码密集型工作中不会发生。

总结：DeepSeek V4 Flash 不会改变你的商业模式 —— token 成本本来就不是问题 —— 但它确实让你在每单位人力监督时间内进一步推动代理自主性，而这才是 2-3 人能够同时运行多少个并发项目的真正限制因素。

参考：

- [DeepSeek V4 Flash — 基准测试、定价及 Flash vs Pro](https://codersera.com/blog/deepseek-v4-flash-deep-dive/)
- [DeepSeek V4 Flash 评测 — CodingFleet](https://codingfleet.com/blog/deepseek-v4-flash-review-028-developer/)
- [DeepSeek V4 Flash — API 定价与基准测试，OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)
- [DeepSeek V4-Pro 评测 — 永久定价、基准测试](https://codersera.com/blog/deepseek-v4-pro-review-benchmarks-pricing-2026/)
