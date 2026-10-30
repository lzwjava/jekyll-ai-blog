---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RULES 和 MRCRv2 基准测试
translated: true
type: note
---

**问题：** 什么是 LLM 的 RULES 和 MRCRv2 attention tests？

**Answer:**

---

## RULES (Rule-Following Language Evaluation Scenarios)

RULES 是一个 programmatic benchmark，旨在评估 Large Language Models 可靠遵循简单明确规则的能力。每个场景包含一个 programmatic evaluation function，通过 string comparison 和 regular expressions 自动检测 rule violations，从而消除了主观人类判断的需要。

关键发现：

- Alignment fine-tuning（如 Llama-2 Chat 和 Gemma IT）令人惊讶地 **降低** 了在此 benchmark 上的 rule-following 表现。
- Harmless rule scores 与现有其他 benchmark 的相关性几乎为零，表明 RULES 衡量的是 LLM 中一种 **根本不同** 的能力。
- 评估涵盖了 proprietary models（GPT-4、Claude、Gemini）和超过 100 个 open-weight models。

---

## MRCRv2 (Multi-Round Coreference Resolution v2)

MRCRv2 是一个增强版的 synthetic long-context reasoning task。它扩展了原始 MRCR framework，加入了 improved evaluation criteria 和 additional complexity，用于测试模型在 extended contexts 中 **保持 attention 和 reasoning** 的能力。

核心思想是 "Latent Structure Queries" (LSQ) framework —— 任务要求模型 "chisel away" 上下文中的无关信息以揭示 latent structure，然后查询模型关于该结构的细节。这为 long-context language model capabilities 提供了更强的信号。

关键变体：

- **MRCR v2 (8-needle)**：从长上下文中检索 8 个 needle items。Meta 的 Muse Spark 1.3 目前以 0.985 的得分领先。
- **MRCR v2 (8-needle, 512K–1M)**：在 512K 到 1 百万 tokens 的上下文上进行评估，目前由 OpenAI 模型领先。
- MRCRv2 在 benchmark scoring systems 中权重显著 —— 贡献了 Reasoning category score 的 20%。

---

**简而言之：**

| Benchmark | 测试 | 关键挑战 |
| --- | --- | --- |
| **RULES** | 规则遵循服从 | LLM 经常违反明确指令 |
| **MRCRv2** | 长上下文 attention & retrieval | 在 512K–1M token 上下文中跟踪多个项目 |

**参考文献：**

- [RULES Paper (arXiv)](https://arxiv.org/abs/2311.04235)
- [MRCRv2 Paper (arXiv)](https://arxiv.org/abs/2409.12640)
- [MRCRv2 Leaderboard - LLM Stats](https://llm-stats.com/benchmarks/mrcr-v2)
