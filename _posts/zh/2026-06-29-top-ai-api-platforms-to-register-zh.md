---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶级AI API平台注册
translated: true
type: note
---

问题：除了 Together.ai、OpenRouter、Jina AI 之外，还有哪些值得注册的 AI/LLM API 平台？

答案：

以下是一个精选列表（不包括你已有的三个），按实际用途分组。跳过那些与你现有平台重叠的。

**推理聚合器 / 多模型网关（OpenRouter 级别）**
- **Fireworks.ai** — 快速无服务器推理，在开放模型和函数调用方面表现强劲，使用 FireAttention 内核。是 Together 的不错替代品。
- **DeepInfra** — 按 token 计费的开放模型托管，通常比 Together/Fireworks 便宜。
- **Novita.ai** — 推理价格低 + GPU 租赁，适合批量处理。
- **Hyperbolic** — 开放权重推理价格低 + 按需 GPU（H100/MI300X spot），适合你的训练工作。
- **Groq** — LPU 推理，Llama/Qwen/Kimi 的每秒 token 数极高。仅用于延迟实验就值得一试。
- **Cerebras** — 晶圆级推理，某些模型甚至比 Groq 更快。有免费层。

**前沿实验室（直接使用，用于评估/智能体工作）**
- **DeepSeek** (platform.deepseek.com) — 你已经大量使用 DeepSeek；直接 API 比转售更便宜，并且能第一时间获得 v4。
- **Moonshot / Kimi** (platform.moonshot.cn) — Kimi K2 是一个强大的智能体/编码模型，价格低廉。
- **Z.ai / Zhipu GLM** — GLM-4.6 是一个严肃的编码模型，OpenRouter 有定价，但直接使用更便宜。
- **Mistral** (la Plateforme) — 用于 Codestral、嵌入和欧盟托管需求。
- **xAI** (Grok API) — 如果你想在智能体轮换中使用 Grok。

**GPU 租赁（训练、MI300X/4070 溢出）**
- **RunPod** — 无服务器 + pods，社区云价格低。最佳的 Together 级别 GPU 租赁。
- **Vast.ai** — 现货市场 GPU，如果你能容忍波动，最便宜的 H100/4090。
- **Lambda** — 干净的 H100/B200 按需服务，适合多 GPU 训练任务。
- **Modal** — 无服务器 Python，非常适合你的 CLI 智能体 / 训练脚本风格（装饰一个函数，在 H100 上运行）。
- **Prime Intellect** — 聚合 GPU 市场，专注于去中心化训练，符合你的 nanoGPT/MoE 兴趣。

**嵌入 / 检索 / 重排序（Jina 级别）**
- **Voyage AI**（现为 Anthropic 旗下）— 顶级的检索嵌入 + 重排序器。
- **Cohere** — Embed v3 + Rerank，适用于 RAG 评估。
- **Nomic** — 开放嵌入 + 用于数据集可视化的 Atlas，适合你的数据工程工作。

**工具相关（值得注册）**
- **Replicate** — 通过 API 运行/微调任何开放模型，适合一次性实验。
- **Baseten** — 基于 Truss 的模型部署，如果你想部署自己的 GPT-2 / 微调模型。
- **Fal.ai** — 如果你涉及图像/音频，快速的多媒体/扩散推理。

如果必须为你的发展路线挑选五个最值得关注的：**Groq**（延迟），**DeepInfra** 或 **Hyperbolic**（廉价 token），**RunPod** + **Modal**（训练/部署），**Voyage**（嵌入）。其余视情况而定。

需要我写一个 Python 脚本，在 OpenRouter + Together + Groq + DeepInfra 上对同一提示词进行基准测试（每秒 token 数、TTFT、每百万 token 成本），让你基于实证而非列表进行排名吗？