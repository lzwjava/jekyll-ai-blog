---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 开源核心与托管服务
translated: true
type: note
---

**问题：SGLang 的商业模式是什么——开源项目如何变现？**

**答案：SGLang 已分为两个方向：**

**1. 开源核心保持免费，由非营利组织托管**
代码仓库仍托管在 LMSYS（非营利组织）下。SGLang 目前由非营利开源组织 LMSYS 维护，有意大规模采用的企业——技术咨询、赞助、合作——可直接联系他们。该项目也获得了资助资金而非收入——2025 年中旬获得了 a16z 第三批开源 AI 资助。

**2. 商业化分拆：RadixArk**
这才是你问的真正的"商业模式"。Ying Sheng 和 Banghua Zhu（两人均为来自 xAI 和 NVIDIA 的 AI 基础设施资深人士）创立了 RadixArk，该公司以 4 亿美元投后估值完成 1 亿美元种子轮融资，由 Accel 领投，Spark Capital 联合领投。投资方阵容强大：NVentures（英伟达风投部门）、AMD、联发科，以及 Angel 投资人如 Igor Babuschkin（xAI）、Lip-Bu Tan（英特尔 CEO）、John Schulman、Soumith Chintala、Thomas Wolf。

收入机制：RadixArk 继续以开源方式开发 SGLang，同时构建 Miles（一个强化学习框架）等周边工具，并已开始对托管服务收费——这是人工智能基础设施领域常见的"开源核心到托管服务"模式（vLLM 也采取了相同做法）。

因此：**开源核心 + 托管推理服务**，其商业逻辑基于：SGLang 被 xAI 和 Cursor 等公司用于加速推理/训练，优化该层能立即大幅节省服务器成本——经典的"基础设施圈地，变现托管而非代码"策略，与 Databricks 如出一辙（巧合的是，Ion Stoica 也是 Databricks 的创始人——SGLang 起源于他在伯克利的实验室）。

对于你自己的智能体栈（ww/iclaw/zz），这与其说是商业模式模板，不如说是提醒：如果你未使用 RadixArk 的托管服务，就只是在运行免费的开源引擎——目前尚无锁定风险，但需关注他们是否会将性能特性（如 PD 分离、大规模专家并行）限制在付费层级中。

参考来源：
- [RadixArk 以 1 亿美元种子轮启动——BusinessWire](https://www.businesswire.com/news/home/20260505077157/en/RadixArk-Launches-with-$100-Million-in-Seed-Funding-Led-by-Accel-to-Grow-SGLang-and-Democratize-Frontier-AI-Infrastructure)
- [TechCrunch：SGLang 分拆为 RadixArk，估值 4 亿美元](https://techcrunch.com/2026/01/21/sources-project-sglang-spins-out-as-radixark-with-400m-valuation-as-inference-market-explodes)
- [sgl-project/sglang GitHub](https://github.com/sgl-project/sglang)