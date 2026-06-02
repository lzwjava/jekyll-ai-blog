---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenRouter最佳平价编程模型推荐
translated: true
type: note
---

### 通过 OpenRouter 使用 Codex CLI 编程的最佳廉价模型

根据 2025 年最新基准测试、用户讨论和模型排名，以下是在 Codex CLI 中用于编程任务的 GPT-5-Codex 最佳且经济实惠的替代方案。GPT-5-Codex 确实价格昂贵（通常每百万 token 输入 20-50 美元 / 输出 60-150 美元，具体取决于供应商），因此这里重点关注具有强大编程性能且成本效益高的选项。OpenRouter 的按使用量付费模式意味着您只需为处理的 token 付费，许多模型提供免费层级或极低的费率（每百万 token 输入/输出合计低于 1 美元）。

我优先考虑了在 SWE-Bench、HumanEval 或 Aider 等编程基准测试中得分高，同时价格低廉或免费的模型。模型 ID 已格式化，便于在您的 `config.toml` 中使用（例如 `model = "provider/model-name"`）。有关当前确切定价，请查阅 OpenRouter 的模型页面，因为费率可能会有小幅波动。

#### 首选推荐：
- **Grok Code Fast (xAI)**
  模型 ID：`xai/grok-code-fast`
  推荐理由：在 OpenRouter 的 LLM 编程排行榜上名列前茅，在速度和代理任务方面表现出色（例如，在国际信息学奥林匹克竞赛中排名第一）。基础使用通常免费，使其成为该平台上使用最广泛的模型。非常适合迭代式编程工作流。
  价格：免费或约 $0.50/$2.00 每百万 token（输入/输出）。上下文长度：128K token。

- **Kat Coder Pro (KwaiPilot)**
  模型 ID：`kwaipilot/kat-coder-pro:free`
  推荐理由：专用编程模型，在 SWE-Bench Verified 上达到 73.4%，接近顶级专有模型。限时免费，非常适合复杂推理和代码生成。
  价格：免费（促销期）。上下文长度：256K token，输出最长 32K。

- **DeepSeek Coder V3 (DeepSeek)**
  模型 ID：`deepseek/deepseek-coder-v3`
  推荐理由：卓越的性价比，在 Aider 编程评分中约 71%，在实现和调试方面表现强劲。论坛中常被推荐用于预算编程。
  价格：非常便宜（约 $0.14/$0.28 每百万 token）。上下文长度：128K token。

- **Llama 4 Maverick (Meta)**
  模型 ID：`meta/llama-4-maverick`
  推荐理由：免费层级中编程质量和 VS Code 集成（例如与 RooCode 等工具）的最佳选择。在实际代码任务中表现良好。
  价格：提供免费层级，或低成本（约 $0.20/$0.80 每百万 token）。上下文长度：128K token。

- **Mistral Devstral Small (Mistral)**
  模型 ID：`mistral/devstral-small`
  推荐理由：针对价格、高吞吐量和良好的代码实现能力进行了优化。常与大型模型搭配用于混合工作流。
  价格：便宜（约 $0.25/$1.00 每百万 token）。上下文长度：128K token。

- **Qwen3 235B (Qwen)**
  模型 ID：`qwen/qwen3-235b`
  推荐理由：在编程基准测试中表现优异，推荐用于成本优化的设置。能很好地处理大规模代码项目。
  价格：经济实惠（约 $0.50/$2.00 每百万 token）。上下文长度：128K token。

- **Gemini 2.5 Flash (Google)**
  模型 ID：`google/gemini-2.5-flash`
  推荐理由：在排行榜上位列第三，对于迭代式编程快速且成本低。如果您的代码涉及数据可视化，也适合多模态任务。
  价格：便宜（约 $0.35/$1.05 每百万 token）。上下文长度：1M token。

这些模型都与 OpenAI 兼容，因此在 Codex CLI 中将提供商设置为 "openrouter" 并配置您的 API 密钥后即可无缝使用。可以从 Grok Code Fast 或 Kat Coder 等免费模型开始测试。对于特定编程用途，请查看 SWE-Bench 分数——分数越高表示解决真实 GitHub 问题的能力越强。如果需要更多上下文长度或速度，可以结合 OpenRouter 的路由功能自动回退到更便宜的模型。

集成方法：在您的 `config.toml` 中添加一个配置块，例如 `[profiles cheap-coder]`，并设置 `model_provider = "openrouter"` 和 `model = "上述 ID 之一"`。

[2025 年 OpenRouter 顶级 AI 模型：性能与成本指南](https://www.teamday.ai/blog/top-ai-models-openrouter-2025)
[2025 年最佳预算编程 LLM：DeepSeek R1 vs Gemini vs GPT](https://llmx.de/blog/budget-coding-llms-2025/)
[OpenRouter 上有哪些可用于编程的最佳 LLM](https://medium.com/@okreitz/what-are-the-best-llms-available-on-openrouter-to-use-for-coding-with-kilo-ca04e75a84ee)
[您可以在 OpenRouter 上使用的最佳免费 AI 模型](https://apidog.com/blog/free-ai-models/)
[2025 年顶级 AI 编程模型](https://www.veerotech.net/blog/top-ai-coding-models-in-2025-boost-your-development-workflow-with-these-game-changers/)
[LLM 排行榜 - OpenRouter](https://openrouter.ai/rankings)
[2025 年 3 月五大 AI 编程模型](https://dev.to/apipie-ai/top-5-ai-coding-models-of-march-2025-5f04)
[模型 - OpenRouter](https://openrouter.ai/models)
[openrouter 上最好的编程模型是什么？ - Reddit](https://www.reddit.com/r/RooCode/comments/1kdu7we/whats_the_best_coding_model_on_openrouter/)
