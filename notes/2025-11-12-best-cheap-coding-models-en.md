---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Best Cheap Coding Models via OpenRouter
translated: false
type: note
---

### Best Cheap Models for Coding with Codex CLI via OpenRouter

Based on recent benchmarks, user discussions, and model rankings as of 2025, here are some of the best and most affordable alternatives to GPT-5-Codex for coding tasks in Codex CLI. GPT-5-Codex is indeed pricey (often in the $20-50 input / $60-150 output per million tokens range, depending on the provider), so these focus on cost-effective options with strong coding performance. OpenRouter's pay-per-use model means you only pay for tokens processed, and many have free tiers or very low rates (under $1 per million tokens combined for input/output).

I've prioritized models with high scores on coding benchmarks like SWE-Bench, HumanEval, or Aider, while being cheap or free. Model IDs are formatted for easy use in your `config.toml` (e.g., `model = "provider/model-name"`). For exact current pricing, check OpenRouter's models page, as rates can fluctuate slightly.

#### Top Recommendations

- **Grok Code Fast (xAI)**
  Model ID: `xai/grok-code-fast`
  Why: Tops OpenRouter's LLM rankings for coding, excels in speed and agentic tasks (e.g., #1 in International Olympiad in Informatics). Often free for basic use, making it the most used model on the platform. Great for iterative coding workflows.
  Price: Free or ~$0.50/$2.00 per 1M tokens (input/output). Context: 128K tokens.

- **Kat Coder Pro (KwaiPilot)**
  Model ID: `kwaipilot/kat-coder-pro:free`
  Why: Specialized coding model with 73.4% on SWE-Bench Verified, close to top proprietary models. Free for a limited time, ideal for complex reasoning and code generation.
  Price: Free (promo). Context: 256K tokens, output up to 32K.

- **DeepSeek Coder V3 (DeepSeek)**
  Model ID: `deepseek/deepseek-coder-v3`
  Why: Excellent value with ~71% on Aider coding scores, strong for implementation and debugging. Frequently recommended for budget coding in forums.
  Price: Very cheap (~$0.14/$0.28 per 1M). Context: 128K tokens.

- **Llama 4 Maverick (Meta)**
  Model ID: `meta/llama-4-maverick`
  Why: Best in free tier for coding quality and VS Code integration (e.g., with tools like RooCode). Performs well on real-world code tasks.
  Price: Free tier available, or low-cost (~$0.20/$0.80 per 1M). Context: 128K tokens.

- **Mistral Devstral Small (Mistral)**
  Model ID: `mistral/devstral-small`
  Why: Optimized for price, fast throughput, and good at code implementation. Often paired with larger models for hybrid workflows.
  Price: Cheap (~$0.25/$1.00 per 1M). Context: 128K tokens.

- **Qwen3 235B (Qwen)**
  Model ID: `qwen/qwen3-235b`
  Why: High performance on coding benchmarks, recommended for cost-optimized setups. Handles large-scale code projects well.
  Price: Affordable (~$0.50/$2.00 per 1M). Context: 128K tokens.

- **Gemini 2.5 Flash (Google)**
  Model ID: `google/gemini-2.5-flash`
  Why: #3 in rankings, fast and low-cost for iterative coding. Good for multimodal tasks if your code involves data viz.
  Price: Cheap (~$0.35/$1.05 per 1M). Context: 1M tokens.

These models are OpenAI-compatible, so they'll work seamlessly in Codex CLI after setting the provider as "openrouter" and your API key. Start with free ones like Grok Code Fast or Kat Coder to test. For coding-specific use, look at SWE-Bench scores—higher means better at solving real GitHub issues. If you need more context or speed, combine with OpenRouter's routing for auto-fallback to cheaper models.

To integrate: In your `config.toml`, add a profile like `[profiles cheap-coder]` with `model_provider = "openrouter"` and `model = "one-of-the-IDs-above"`.

[Top AI Models on OpenRouter 2025: Performance vs Cost Guide](https://www.teamday.ai/blog/top-ai-models-openrouter-2025)
[Best Budget Coding LLMs 2025: DeepSeek R1 vs Gemini vs GPT](https://llmx.de/blog/budget-coding-llms-2025/)
[What are the best LLMs available on OpenRouter to use for coding](https://medium.com/@okreitz/what-are-the-best-llms-available-on-openrouter-to-use-for-coding-with-kilo-ca04e75a84ee)
[Best Free AI Models You Can Use on OpenRouter](https://apidog.com/blog/free-ai-models/)
[Top AI Coding Models in 2025](https://www.veerotech.net/blog/top-ai-coding-models-in-2025-boost-your-development-workflow-with-these-game-changers/)
[LLM Rankings - OpenRouter](https://openrouter.ai/rankings)
[Top 5 AI Coding Models of March 2025](https://dev.to/apipie-ai/top-5-ai-coding-models-of-march-2025-5f04)
[Models - OpenRouter](https://openrouter.ai/models)
[whats the best coding model on openrouter? - Reddit](https://www.reddit.com/r/RooCode/comments/1kdu7we/whats_the_best_coding_model_on_openrouter/)
