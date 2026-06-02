---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenRouter与直接API成本对比
translated: true
type: note
---

是的，通过 OpenRouter API 访问相同模型通常比直接使用 DeepSeek、Mistral、Google（Gemini）或 xAI（Grok）等官方供应商的 API 成本更高。OpenRouter 声称会透传底层供应商的定价，不在推理成本上加价，但他们收取的附加费用会增加总体开支：

- 通过标准支付方式购买额度时收取 5.5% 手续费（最低 0.80 美元），加密货币支付额外加收 5%
- 即使为支持的供应商自带 API 密钥（BYOK），OpenRouter 仍会从您的 OpenRouter 额度中扣除 5% 费用（基于其预估的模型成本）

这些费用实际上使 OpenRouter 比直接访问贵出 5-5.5%，外加根据使用量和支付方式可能产生的固定最低费用。直接访问可避免这些额外支出，您只需支付供应商的令牌费率。

### 成本对比示例

以下是根据现有定价数据的粗略对比（以每百万令牌美元计；请注意费率可能因模型版本、时间段、缓存或区域而异——请始终查阅官方网站获取最新信息）。OpenRouter 的基础令牌费率与供应商保持一致（透传），但会叠加上述费用。

- **DeepSeek**：
  - 直接访问：输入约 0.14–0.55 美元（缓存命中/未命中），输出约 1.10–2.19 美元（因模型和折扣时段而异）
  - OpenRouter：相同基础费率 + 5–5.5% 附加费

- **Mistral**：
  - 直接访问：输入约 2.00 美元（Large 2 模型），输出约 6.00 美元（基于混合费率估算；旧版 Small 模型约为输入 0.15 美元/输出 0.50 美元）
  - OpenRouter：相同基础费率 + 5–5.5% 附加费

- **Gemini（Google）**：
  - 直接访问：不同模型差异较大（例如 Gemini 1.5 Pro：输入 1.25–2.50 美元，输出 5.00–10.00 美元；Gemini 1.5 Flash：输入 0.075–0.15 美元，输出 0.30–0.60 美元）
  - OpenRouter：相同基础费率 + 5–5.5% 附加费（Google 可能支持 BYOK）

- **Grok（xAI）**：
  - 有关 Grok API 定价和访问详情，请访问 <https://x.ai/api。根据公开信息，Grok-3/Grok-4> 费率约为输入 3.00 美元/输出 15.00 美元，Grok-3-mini 约为输入 0.30 美元/输出 0.50 美元
  - OpenRouter：相同基础费率 + 5–5.5% 附加费（xAI 通常未提及 BYOK）

如果您的使用量很大，百分比附加费会快速累积。对于低频使用或测试场景，差异可能不明显，但直接访问仍然更便宜。OpenRouter 的价值在于其统一 API 和路由功能，这些便利性可能值得您支付额外成本。

[OpenRouter 常见问题解答](https://openrouter.ai/docs/faq)
[DeepSeek API 定价](https://api-docs.deepseek.com/quick_start/pricing)
[Mistral AI 定价](https://mistral.ai/pricing)
[Google Gemini API 定价](https://ai.google.dev/pricing)
[xAI API](https://x.ai/api)
[Mistral Large 2 分析报告](https://artificialanalysis.ai/models/mistral-large-2)
[DeepSeek 定价指南](https://team-gpt.com/blog/deepseek-pricing/)
