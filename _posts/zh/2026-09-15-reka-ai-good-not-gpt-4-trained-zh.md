---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Reka AI：好，但未使用GPT-4训练
translated: true
type: note
---

**问题：** 什么是 Reka AI，它表现如何，以及它是否在一年内使用 GPT-4 进行了训练？

---

**回答：**

**什么是 Reka AI？**

Reka AI 是一家面向企业的前沿人工智能实验室，从头开始设计多模态基础模型。它由前 Google DeepMind、Google Brain、Meta FAIR 和百度研究员于 2022 年创立。

该公司专注于超高效训练与服务基础设施，以低成本提供推理能力。其旗舰产品是 **Reka Flash**，一种能够理解视频、图像、文本和音频的多模态模型。它还提供 **Reka Vision**（视觉搜索与视频理解）和 **Reka Research**（代理式网络研究平台）。

**它表现如何？**

是的，它备受好评，特别是在多模态任务方面：

- 在盲测第三方评估中，Reka Core 在**多模态聊天**中排名**第二**，仅次于 GPT-4V，领先于所有 Claude 3 模型。在纯文本聊天中，它排名第三，仅次于 GPT-4 Turbo 和 Claude 3 Opus。
- 其模型系列——Spark (1B)、Edge (7B)、Flash (21B) 和 Core (67B)——涵盖了从轻量级嵌入式应用到重型企业工作负载的各种场景。Reka Vision 是其最成熟的产品，能够对大型视频档案进行自然语言语义搜索。
- 截至 2025 年 7 月，Reka 获得了 NVIDIA 和 Snowflake 支持的 1.1 亿美元融资，估值达到 10 亿美元，成为独角兽。
- 2026 年 6 月，Reka 与物理人工智能初创公司 Moonvalley 合并，进军世界模型和机器人领域。

主要缺点：该平台缺乏透明的公开定价，明确面向 B2B/开发者，使得非技术用户或小团队较难使用。

**它是否在一年内使用 GPT-4 进行了训练？**

**不——这是一种误解。** Reka Core 是一个从头开始训练的Transformer模型，使用了公开和专有数据的混合，包括文本、图像、视频和音频片段。它并非从 GPT-4 蒸馏而来，也未使用 GPT-4 进行训练。Reka Core 在短短几个月内从头开发，主要基于 NVIDIA H100 和 A100 GPU 进行训练。这种混淆可能源于它的*性能* **可与 GPT-4 媲美**，而非它是基于 GPT-4 构建的。

---

**参考资料：**

- [Reka AI Wiki](https://aiwiki.ai/wiki/reka_ai)
- [Reka Core vs GPT-4 — The Decoder](https://the-decoder.com/reka-core-is-the-next-multimodal-ai-model-that-makes-gpt-4-seem-less-special/)
- [Reka 1.1 亿美元融资公告](https://reka.ai/news/reka-secures-110-million-to-accelerate-adoption-of-its-multimodal-ai-platforms)
- [Reka 2026 年评测](https://comparateur-ia.com/en/reviews/reka)
