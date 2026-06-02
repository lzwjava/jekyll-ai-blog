---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenRouter Model Token Pricing Guide
translated: false
type: note
---

Here’s what those exact OpenRouter models currently cost per **1M tokens** (input → output). I’m pulling straight from each model’s page:

* **Anthropic Claude Opus 4** — **\$15 → \$75** (images: \$24/K). ([OpenRouter][1])
* **Anthropic Claude Sonnet 4** — **\$3 → \$15** (images: \$4.80/K). ([OpenRouter][2])
* **Google Gemini 2.5 Flash** — **\$0.30 → \$2.50** (images: \$1.238/K). ([OpenRouter][3])
* **Google Gemini 2.5 Pro** — **\$1.25 → \$10** (page lists “starting at”). ([OpenRouter][4])
* **DeepSeek V3** — **\$0.18 → \$0.72**. ([OpenRouter][5])
* **Moonshot Kimi K2** — **\$0.14 → \$2.49**. ([OpenRouter][6])
* **Mistral Medium 3.1** — **\$0.40 → \$2.00**. ([OpenRouter][7])
* **Qwen3 Coder** — **\$0.20 → \$0.80** *(note: higher tier kicks in past 128k input tokens)*. ([OpenRouter][8])
* **OpenAI GPT-OSS 120B** — **\$0.073 → \$0.29**. ([OpenRouter][9])
* **OpenAI GPT-5** — **\$1.25 → \$10**. ([OpenRouter][10])

Quick tips & gotchas:

* Your mapping has **two `deepseek-v3` keys**; in Python dicts the **later one overwrites the earlier**. If you want both paid and `:free` routes, use distinct keys (e.g., `"deepseek-v3-free"` vs `"deepseek-v3"`).
* Some models have **`:free`** routes (useful for quick tests but rate-limited): e.g., `qwen/qwen3-coder:free` and `moonshotai/kimi-k2:free`. ([OpenRouter][11])

If you want, I can compute example request costs for your typical prompt/response token sizes.

[1]: https://openrouter.ai/anthropic/claude-opus-4 "OpenRouter"
[2]: https://openrouter.ai/anthropic/claude-sonnet-4 "OpenRouter"
[3]: https://openrouter.ai/google/gemini-2.5-flash "OpenRouter"
[4]: https://openrouter.ai/google/gemini-2.5-pro "OpenRouter"
[5]: https://openrouter.ai/deepseek/deepseek-chat "OpenRouter"
[6]: https://openrouter.ai/moonshotai/kimi-k2 "OpenRouter"
[7]: https://openrouter.ai/mistralai/mistral-medium-3.1 "OpenRouter"
[8]: https://openrouter.ai/qwen/qwen3-coder "OpenRouter"
[9]: https://openrouter.ai/openai/gpt-oss-120b?utm_source=chatgpt.com "gpt-oss-120b - API, Providers, Stats"
[10]: https://openrouter.ai/openai/gpt-5?utm_source=chatgpt.com "GPT-5 - API, Providers, Stats"
[11]: https://openrouter.ai/qwen/qwen3-coder%3Afree?utm_source=chatgpt.com "Qwen3 Coder (free) - API, Providers, Stats"
