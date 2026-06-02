---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为盘古大模型 Ultra 135B 概述
translated: true
type: note
---

Question: 什么是华为的 Pangu 135B V3 模型？

Answer:

## Huawei Pangu 135B V3 ("Pangu Ultra")

**135B V3** 是由 Huawei **Noah's Ark Lab** 开发的 Pangu AI 计划中的第三版、拥有 135 billion 参数的 dense 架构 large language model。其官方品牌名称为 **Pangu Ultra**。

---

### 技术规格

Pangu Ultra 是一个拥有 **135 billion parameters** 和 **128K context window** 的 dense LLM，在 **8,192 颗 Ascend 910B NPU**（Huawei 自研 AI 芯片）上使用 **13.2 trillion tokens** 训练而成。

该模型包含 **94 neural layers**，并采用了三阶段训练方案：第一阶段涵盖 12 trillion tokens 的通用知识；第二阶段增加 0.8 trillion tokens 用于 reasoning（数学和代码）；第三阶段使用 curriculum learning 处理复杂的 Q&A 对。

为了解决如此深度下的训练不稳定性，Huawei 引入了 **Depth-Scaled Sandwich Normalization (DSSN)** 和 **TinyInit**，与 Meta 的 Llama 3 方法相比，这将训练中的 loss spikes 减少了 78%。

它取得了强劲的 benchmark 结果，超越了 LLaMA-3 (405B dense) 和 Qwen2.5 (72B) 等模型，并且尽管是一个规模较小的纯 dense 模型，仍能与 DeepSeek-R1 (671B MoE) 竞争。

---

### "V3" 的重要意义 —— 来自举报丑闻的背景

由于 2025 年中曝光的一场重大内部争议，**V3** 标签显得尤为重要。根据一名来自 Huawei Noah's Ark Lab 的举报者透露：

- **135B V1 和 V2** 据称是通过“套壳”构建的 —— 即重新包装竞争对手的模型（特别是 Alibaba 的 Qwen-110B），进行表面修改，并将其作为自主研发成果展示。

- 然而，**135B V3** 是个例外。核心团队在 Ascend 硬件上完整地从零开始训练了 135B V3 "Pangu Ultra" 模型 —— 没有走捷径，没有盗用代码 —— 训练过程稳定，没有出现 loss spikes，性能可靠且达到了竞争对手的 benchmark 水平。

- 举报者称其为团队真正的骄傲，写道内部人员“愿意用生命和荣誉担保这一模型训练的真实性”，并描述了一个经历了无数次 rollback 以确保稳定性的艰辛过程。

- 与涉嫌抄袭的 V2 不同，135B V3 使用了精炼的 tokenizer 和改进的训练 pipeline —— 被描述为“血汗与牺牲的真实产物” —— 实现了没有 loss spikes 的干净训练。

---

### 为什么它很重要

135B V3 在内部被视为 Huawei 第一次真正具有竞争力的、诚实的尝试，证明了 Huawei 的 Ascend 芯片确实可以从零开始训练大规模模型，而不依赖于 NVIDIA 硬件 —— 考虑到持续的美国制裁，这是一个重大的地缘政治和技术声明。

Huawei 还应用了 DSSN 和 TinyInit 帮助模型在 Ascend 芯片上实现了超过 52% 的 MFU (Model FLOP Utilization)，这是一个显著的硬件效率成果。

---

### 摘要表

| 属性 | 详情 |
|---|---|
| 模型名称 | Pangu Ultra (135B V3) |
| Parameters | 135 billion (dense) |
| Context Window | 128K tokens |
| Training Tokens | 13.2 trillion |
| 硬件 | 8,192 Ascend 910B NPUs |
| 关键技术 | DSSN, TinyInit, NPU Fusion Attention |
| 状态 | 真正从零开始训练（根据举报者消息） |

参考文献：

- [The Pangu Illusion – Open Source Ward](https://www.open-source-ward.com/the-pangu-illusion-how-huaweis-star-ai-model-was-built-on-burnout-betrayal-and-open-source-theft/)
- [Huawei PanGu – Wikipedia](https://en.wikipedia.org/wiki/Huawei_PanGu)
- [The Latest Huawei AI Scandal – Medium](https://medium.com/@PlanB./the-latest-huawei-ai-scandal-unlocking-the-secret-fraud-behind-pangus-fall-e171cce1f075)
- [Pangu Ultra Technical Overview – zqg8.com](https://www.zqg8.com/post/383.html)
- [Whistleblower: Huawei cloned Qwen and DeepSeek – Dilemma Works](https://dilemmaworks.substack.com/p/whistleblower-huawei-cloned-and-renamed)
- [How Huawei Trains LLMs Using Ascend Chips – Recode China AI](https://recodechinaai.substack.com/p/how-huawei-trains-deepseek-r1-class)
- [Whistleblower Exposes Alleged Fraud – CTOL Digital Solutions](https://www.ctol.digital/news/whistleblower-exposes-alleged-fraud-misconduct-huawei-flagship-ai-program/)
