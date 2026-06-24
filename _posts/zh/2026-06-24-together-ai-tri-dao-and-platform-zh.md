---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Together AI: 特里·道和平台'
translated: true
type: note
---

**问题：** Together AI 具体是做什么的？Tri Dao 在那里工作吗？

**回答：**

是的——Tri Dao 是 Together AI 的**联合创始人兼首席科学家**，而不仅仅是员工。他是五位联合创始人之一，其他四位包括 Vipul Ved Prakash（CEO）、Ce Zhang（CTO）、Chris Ré 和 Percy Liang——这些人都是斯坦福/卡内基梅隆大学系统与机器学习研究领域的重磅人物。

**Together AI 是什么：**

Together AI 是一个面向生产级 AI 的全栈 AI 平台，以前沿系统研究为驱动——帮助团队更快交付、可靠扩展，并实现更优的单位经济性。具体来说，它包含三部分：

1.  **推理 API** —— 为开源模型（Llama、Qwen、Mistral、DeepSeek 等）提供快速、低成本的推理服务。实际基准测试显示，其 TPS（每秒 token 数）比 TensorRT-LLM 高 31%，在饱和状态下 TTFT（首 token 生成时间）提升 2 倍，成本比 Claude Opus 4.6 低 76%。

2.  **微调平台** —— 在其 GPU 基础设施上提供托管式微调服务，近期升级支持更大模型和更长上下文。

3.  **系统研究** —— 这是它的差异化优势。他们发布了 ATLAS（自适应学习推测系统，AdapTive-LeArning Speculator System），这是一种运行时学习加速器，可将 LLM 推理速度提升高达 4 倍，并且进行深度的内核级研究（Dan Fu 担任内核副总裁）。

**Tri Dao 的具体角色：**

他还是普林斯顿大学计算机科学系的助理教授，领导 Dao AI Lab，专注于硬件感知算法和具备长程记忆的序列模型。你应该了解他的两项代表性工作：

-   **FlashAttention / FlashAttention-2** —— 具备 IO 感知的精确注意力机制，现已成为所有严肃训练栈的标准配置。FA-2 在 A100 上实现了 72% 的模型 FLOPs 利用率，与前一版本相比，训练速度提升高达 4 倍。
-   **Mamba**（与 Albert Gu 合作）—— 基于 SSM（状态空间模型）的 Transformer 替代方案，与“超越 Transformer”的浪潮密切相关。Together AI 基于此发布了 StripedHyena 和混合架构的相关论文。

**这对你为何重要：**

如果你正在基于开源模型构建产品，Together AI 是 OpenAI API 的最佳替代方案之一——具有竞争力的定价、针对 FlashAttention 优化的推理服务，以及背后真实的系统研究（而不仅仅是转售 GPU 算力）。鉴于你已经在使用 OpenRouter 和 DeepSeek，对于延迟敏感型工作负载（尤其是 Llama/Qwen 的推理场景），Together AI 值得进行基准测试。

**参考链接：**

-   [Together AI - Tri Dao 公告 + FA-2](https://www.together.ai/blog/tri-dao-flash-attention)
-   [Tri Dao 的个人主页](https://tridao.me/tridao.github.io/)
-   [Together AI 关于页面](https://www.together.ai/about-us)