---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 代理的最佳模型
translated: true
type: note
---

**问题：** 哪些模型适合在 OpenClaw 中使用？

**答案：**

OpenClaw 是一个开源的、本地优先的个人 AI agent 框架（本身不是 LLM），它通过 API 或本地服务器连接到外部 large language models。它在具有强大 tool-calling 可靠性、对指令低 hallucination、良好 long-context 处理以及错误恢复能力的模型上表现出色——因为它运行 persistent、多步骤 agent loops（browser、file ops、shell、emails 等）。

截至 2026 年 3 月，以下是基于社区使用、docs、Reddit/Discord 反馈以及实际 tier lists 的最推荐和备受推崇的 OpenClaw 模型：

### 顶级层级 (S/A — 最适合严肃 agent 工作的可靠模型)
- **Anthropic Claude family** (especially Sonnet 4 / Opus 4.5 / Opus 4.6)
  仍然被广泛认为是 OpenClaw 的黄金标准。极度一致的 JSON/tool calling，在多步骤推理方面出色，能够很好地从部分失败中恢复，并且在不丢失跟踪的情况下处理长上下文。
  - 大多数用户的最佳默认选择（日常任务、coding、research）。
  - 对于成本/推理平衡，从 Sonnet 开始；对于复杂生产代码或深度任务，使用 Opus。

- **Moonshot Kimi series** (Kimi K2.5, Kimi K2 Thinking)
  非常受欢迎（尤其在中国），推理能力强、多模态、支持 sub-agent，并且性价比高。在 agentic workflows 中经常位居社区投票榜首。

- **MiniMax models** (M2.5, MiMo-V2-Flash)
  快速、高效用于 coding/productivity，优秀的本地/offline 性能（via LM Studio），低成本。通常用于 heartbeats/后台任务或完整的本地栈。

- **DeepSeek family** (DeepSeek V3.2, DeepSeek R1, DeepSeek-Coder)
  出色的性价比，强大的 coding/math，可靠的工具使用在 agent loops 中。经常被推荐用于预算有限或高容量使用。

### 强大的本地 / 自托管选项 (via Ollama, LM Studio, llama.cpp)
这些选项完全私有、无 API 成本（需要合适的硬件，例如 32GB+ RAM 的 Mac/PC 或 GPU）：
- **Qwen series** (Qwen3-Coder 32B, Qwen3.5 variants, GLM-4.7 / GLM-5) — 顶级本地选择；非常稳定的 tool calling、高上下文、社区对 OpenClaw 的最爱。
- **Devstral-Small-2-24B** 或类似 fine-tuned coding models — 在生产 agent 设置中已被证明可靠。
- **Llama 3.3 70B / Llama 4 variants** — 当良好 quantized 时，具有坚实的通用性能。

### 其他经常提到的优秀表现者
- Google Gemini (3 Pro / 2.5 Flash) — 非常适合 research/speed，原生长上下文。
- OpenAI GPT family (GPT-5 series, GPT-4o) — 庞大的生态系统支持，但一些用户报告在长 agent 会话中 tool 一致性不如 Claude 可靠。

### 快速决策指南 (2026 社区共识)
- **最佳整体可靠性/tool use** → Claude Sonnet/Opus
- **最佳性价比 + 强大 agent 性能** → Kimi K2.5 或 DeepSeek V3.2
- **最佳廉价/快速/heartbeats** → MiniMax Flash, GLM-4.7, Gemini Flash
- **最佳完全本地/隐私** → Qwen3-Coder 32B 或 MiniMax M2.5 via LM Studio/Ollama
- **用于 coding 密集型 agents** → Claude Opus, Qwen3-Coder, DeepSeek-Coder

OpenClaw 原生支持 model routing/failover——许多用户设置强大的主模型（例如 Claude）+ 廉价 fallback（例如 MiniMax 或 DeepSeek）来优化成本和 uptime。请查看 OpenClaw docs 以获取确切的 provider/model strings 和 auth 设置。

**参考资料：**

- [OpenClaw official docs - Models](https://docs.openclaw.ai/concepts/models)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [Best AI Models for OpenClaw in 2026](https://flypix.ai/best-ai-model-openclaw)
- [Reddit r/LocalLLM - LLM recommendations for OpenClaw](https://www.reddit.com/r/LocalLLM/comments/1rcf3y0/looking_for_llm_recommendations_to_use_with)
- [Community tier list discussions](https://www.answeroverflow.com/m/1470980417225101404)
- [Local models guide for OpenClaw](https://docs.openclaw.ai/gateway/local-models)
