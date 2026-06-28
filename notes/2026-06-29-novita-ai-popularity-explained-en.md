---
audio: false
generated: true
image: false
lang: en
layout: post
title: Novita AI Popularity Explained
translated: false
type: note
---

Question: How popular is Novita AI (novita.ai), the inference provider that shows up as a Hugging Face login/inference partner?

Answer:

Let me search for current data rather than guess.Novita AI is one of the more popular serverless inference providers in the HF ecosystem right now, not a fringe option.

What the "login/integration" you saw actually is: HF's **Inference Providers** routing layer. Novita is registered as a provider, so when you hit `https://router.huggingface.co/v1` with your `HF_TOKEN`, HF can route your request to Novita's backend. You can run in two modes — HF-routed (HF bills you, PRO users get $2/month credits) or custom-key (you add a Novita API key and get billed on your Novita Studio account directly). That dual-billing setup is what felt novel to you.

On popularity:

- It became an **official HF Inference Partner** in April 2026, serving the 5M+ HF developer base, and was a day-0 launch partner for Gemma 4. Novita AI and Hugging Face announced a strategic partnership to bring affordable, reliable inference for the latest AI models to over five million developers on Hugging Face, and Novita was a day 0 launch partner for Gemma 4.
- It's adopted beyond HF — Novita AI is trusted by leading teams across the AI ecosystem, including Hugging Face, Quora, OpenRouter, Vercel, Kilo Code, and Genspark. So you're likely already routing through it indirectly via OpenRouter.
- Scale: the platform covers more than 120 large language models through a single OpenAI-compatible and Anthropic-compatible API and makes every new model available on release day.
- Benchmarks back the marketing somewhat — on Artificial Analysis' GPT-OSS-120B provider benchmarks (April 2026), Novita ranked #1 on GPQA Diamond at 79.0%, hit 93.3% on AIME 2025, and placed #5 on IFBench at 68.9%.

Practical angle for you: it's a real competitor to Together AI / Fireworks / Groq, positioned on cost (claims up to 50% cheaper) and day-0 model availability. Since you already burn ~2B tokens through OpenRouter, the interesting move is to A/B Novita's direct endpoint against your current routes for the open models you use most (DeepSeek V4, Qwen, GLM) — OpenAI-compatible API means it's a one-line `base_url` swap:

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.novita.ai/v3/openai", api_key="<​API_KEY>")
r = client.chat.completions.create(model="deepseek/deepseek-v4-pro", messages=[{"role":"user","content":"ping"}])
```

Or keep it inside HF routing by appending `:novita` to the model id (`deepseek-ai/DeepSeek-V4-Pro:novita`).

One caveat on the popularity read: much of the strongest framing above comes from Novita's own PR and self-commissioned benchmarks, so treat the "#1" and "best performing" claims as vendor-flavored. The trust signals (HF, OpenRouter, Vercel adoption) are the more neutral evidence that it's genuinely widely used.

References:

- [Novita AI Joins Hugging Face as Official Inference Partner](https://www.prnewswire.com/news-releases/novita-ai-joins-hugging-face-as-official-inference-partner-302741097.html)
- [Novita AI Ranked as Best Performing & Reliable Inference Layer](https://www.morningstar.com/news/pr-newswire/20260421sf38721/novita-ai-ranked-as-the-best-performing-reliable-inference-layer)
- [HF Inference Providers — Novita docs](https://huggingface.co/docs/inference-providers/providers/novita)
