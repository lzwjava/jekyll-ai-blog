---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: DeepSeek Token定价细则详解
translated: true
type: note
---

针对您观察到的现象：DeepSeek v32 确实宣布了大幅降价——某些情况下降幅高达50%甚至更多——但用户实际体验到的成本降低可能因以下因素而有所差异：

- **标称价格 vs 实际成本**：DeepSeek 宣布每百万tokens价格从1.68美元降至0.42美元（某些场景下降幅达75%），但这仅针对原始token定价。您的实际成本取决于具体使用模式：输入输出token比例、缓存命中/未命中率，以及是否使用闲时折扣（特定时段优惠幅度可达50-75%）ue202turn0search1,[1],[2]。
- **缓存效率**：若您的工作负载受益于缓存（如重复提示词或上下文复用），实际成本可能低于标称价格，但宣传的降价仅适用于基础费率，不一定适用于缓存token。
- **输入/输出不对称计费**：某些模型对输入输出token采用不同费率。若降价仅适用于输入token而您的任务以输出为主，整体成本降幅将低于50%。
- **闲时折扣**：DeepSeek在闲时段（UTC时间16:30-00:30）提供额外折扣，若您的使用时间与之重合可进一步降低成本ue202turn0search2。

**您未立即看到50%成本下降的原因：**
- 降价可能未统一适用于所有token类型或使用场景
- 您任务的特定token分布（输入/输出、缓存命中/未命中）可能与宣传的降价范围不完全吻合
- 从公告发布到价格变更全面体现在所有计费系统或API可能存在延迟

总之，虽然DeepSeek v32的降价真实且幅度显著，但实际节省成本取决于您的使用模式，未必与宣传百分比完全吻合ue202turn0search1,[1],[2]。

引用来源：
[1] https://x.com/deepseek_ai
[2] https://www.facebook.com/groups/developerkaki/posts/2615893198756577/
