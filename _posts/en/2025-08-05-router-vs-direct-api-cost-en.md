---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenRouter vs Direct API Cost
translated: false
type: note
---

Yes, using OpenRouter APIs to access the same models is generally more costly than using the official APIs directly from providers like DeepSeek, Mistral, Google (for Gemini), or xAI (for Grok). OpenRouter claims to pass through the underlying provider's pricing without adding a markup on the inference costs themselves, but they charge additional fees that increase the overall expense:

- A 5.5% fee (with a $0.80 minimum) when purchasing credits via standard payment methods, plus an extra 5% for crypto payments.
- Even if you bring your own API keys (BYOK) for supported providers, OpenRouter deducts a 5% fee (based on their estimated model cost) from your OpenRouter credits.

These fees effectively make OpenRouter 5-5.5% more expensive than going direct, plus any fixed minimums, depending on your usage and payment method. Direct access avoids these extras, as you only pay the provider's token rates.

### Cost Comparison Examples
Here's a rough comparison based on available pricing data (in USD per million tokens; note that rates can vary by model version, time of day, caching, or region—always check official sites for latest details). OpenRouter's base token rates match the providers (pass-through), but add the fees above.

- **DeepSeek**:
  - Direct: Input ~$0.14–$0.55 (cache hit/miss), Output ~$1.10–$2.19 (varies by model and discount periods).
  - OpenRouter: Same base rates + 5–5.5% fees.

- **Mistral**:
  - Direct: Input ~$2.00 (for Large 2), Output ~$6.00 (estimated based on blended rates; older models like Small were ~$0.15 input/$0.50 output).
  - OpenRouter: Same base rates + 5–5.5% fees.

- **Gemini (Google)**:
  - Direct: Varies widely by model (e.g., Gemini 1.5 Pro: Input $1.25–$2.50, Output $5.00–$10.00; Gemini 1.5 Flash: Input $0.075–$0.15, Output $0.30–$0.60).
  - OpenRouter: Same base rates + 5–5.5% fees (BYOK may be supported for Google).

- **Grok (xAI)**:
  - For details on Grok API pricing and access, visit https://x.ai/api. Based on public info, rates are around Input $3.00/Output $15.00 for Grok-3/Grok-4, or Input $0.30/Output $0.50 for Grok-3-mini.
  - OpenRouter: Same base rates + 5–5.5% fees (BYOK not typically mentioned for xAI).

If your usage is high-volume, the percentage fees add up quickly. For low usage or testing, the difference might be minimal, but direct access is still cheaper. OpenRouter's value comes from its unified API and routing features, which might justify the extra cost for convenience.

[OpenRouter FAQ](https://openrouter.ai/docs/faq)
[DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing)
[Mistral AI Pricing](https://mistral.ai/pricing)
[Google Gemini API Pricing](https://ai.google.dev/pricing)
[xAI API](https://x.ai/api)
[Mistral Large 2 Analysis](https://artificialanalysis.ai/models/mistral-large-2)
[DeepSeek Pricing Guide](https://team-gpt.com/blog/deepseek-pricing/)
