---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenRouter模型代币定价指南
translated: true
type: note
---

以下是当前这些OpenRouter模型每**100万token**的精确费用（输入→输出）。数据直接来自各模型页面：

* **Anthropic Claude Opus 4** — **15美元 → 75美元**（图像：24美元/千张）。([OpenRouter][1])
* **Anthropic Claude Sonnet 4** — **3美元 → 15美元**（图像：4.80美元/千张）。([OpenRouter][2])
* **Google Gemini 2.5 Flash** — **0.30美元 → 2.50美元**（图像：1.238美元/千张）。([OpenRouter][3])
* **Google Gemini 2.5 Pro** — **1.25美元 → 10美元**（页面标注“起始价”）。([OpenRouter][4])
* **DeepSeek V3** — **0.18美元 → 0.72美元**。([OpenRouter][5])
* **Moonshot Kimi K2** — **0.14美元 → 2.49美元**。([OpenRouter][6])
* **Mistral Medium 3.1** — **0.40美元 → 2.00美元**。([OpenRouter][7])
* **Qwen3 Coder** — **0.20美元 → 0.80美元** *（注：超过12.8万输入token后启用更高阶梯价格）*。([OpenRouter][8])
* **OpenAI GPT-OSS 120B** — **0.073美元 → 0.29美元**。([OpenRouter][9])
* **OpenAI GPT-5** — **1.25美元 → 10美元**。([OpenRouter][10])

注意事项与使用技巧：

* 您的配置中存在**两个`deepseek-v3`键名**；在Python字典中**后者会覆盖前者**。若需同时使用付费和`:free`路由，请使用不同键名（如`"deepseek-v3-free"`与`"deepseek-v3"`）。
* 部分模型提供**:free**路由（适用于快速测试但存在速率限制）：例如`qwen/qwen3-coder:free`和`moonshotai/kimi-k2:free`。([OpenRouter][11])

如果需要，我可以根据您典型的提示/响应token量计算具体请求成本。

[1]: https://openrouter.ai/anthropic/claude-opus-4 "OpenRouter"
[2]: https://openrouter.ai/anthropic/claude-sonnet-4 "OpenRouter"
[3]: https://openrouter.ai/google/gemini-2.5-flash "OpenRouter"
[4]: https://openrouter.ai/google/gemini-2.5-pro "OpenRouter"
[5]: https://openrouter.ai/deepseek/deepseek-chat "OpenRouter"
[6]: https://openrouter.ai/moonshotai/kimi-k2 "OpenRouter"
[7]: https://openrouter.ai/mistralai/mistral-medium-3.1 "OpenRouter"
[8]: https://openrouter.ai/qwen/qwen3-coder "OpenRouter"
[9]: https://openrouter.ai/openai/gpt-oss-120b?utm_source=chatgpt.com "gpt-oss-120b - API、提供商、数据统计"
[10]: https://openrouter.ai/openai/gpt-5?utm_source=chatgpt.com "GPT-5 - API、提供商、数据统计"
[11]: https://openrouter.ai/qwen/qwen3-coder%3Afree?utm_source=chatgpt.com "Qwen3 Coder (免费版) - API、提供商、数据统计"
