---
audio: false
generated: true
image: false
lang: en
layout: post
title: ZenMux LLM Gateway with Insurance
translated: false
type: note
---

**Question:** What is ZenMux (zenmux.ai)?

**Answer:**

Let me check what they actually offer rather than guess.**Answer:**

ZenMux is an LLM API gateway/aggregator — same category as OpenRouter, but with a different angle. It gives you one account, one API key, and direct access to 200+ LLMs from every major provider—OpenAI, Anthropic, Google, DeepSeek, Meta, xAI, Moonshot, and more. Drop-in OpenAI/Anthropic/Vertex-compatible endpoints, so zero code changes to swap providers.

The differentiating gimmick is **"LLM Insurance"** — automatic compensation when outputs are hallucinated, latency exceeds thresholds, or throughput drops, no manual claims required. Worth understanding how the detection actually works before taking the "insurance" framing at face value, because it's looser than it sounds: quality is user-defined, triggered by actions like clicking "regenerate" or re-asking a highly similar question — they run a similarity algorithm and if it qualifies, they count it as a case. So it's heuristic (regen clicks, latency spikes, similarity matching), not a real eval model judging correctness. The "data flywheel" pitch — every compensated case is anonymized and fed back to you so you can improve your own product — is the part they're really selling.

Drop-in usage, OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://zenmux.ai/api/v1",
    api_key="<API_KEY>",
)

completion = client.chat.completions.create(
    model="qwen/qwen3-max",   # provider/model naming, like OpenRouter
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(completion.choices[0].message.content)
```

Other facts worth filing:

- They publicly and continuously evaluate model channels via regular Humanity's Last Exam (HLE) tests, open-sourced on GitHub, to detect "degraded" / proxied models. This is the genuinely interesting bit for you — official-source channels with auditable degradation detection, vs. gray-market proxies that quietly serve quantized or throttled models. That's a real failure mode on cheaper aggregators.
- Pricing is per-token, roughly $0.05–$21/M input and $0.40–$168/M output depending on tier, competitive with direct provider rates plus their margin.
- They ran a Feb 2026 promo giving free Claude Opus 4.6 access for a 2-week trial.

**My take for your situation:** Given you're already running ~3B tokens/year across all providers, ZenMux is a sidegrade, not an upgrade, for most of your usage. OpenRouter has far more models (300+), more providers, and a larger battle-tested user base. ZenMux's edges that might matter to you specifically: the **HLE-based source verification** (if you've been burned by degraded channels), and **official-only routing** (no gray-market quantized models silently swapped in). The "insurance" is mostly a marketing hook — the compensation triggers are heuristic and gameable, not a quality guarantee you'd architect around.

If you want to test it, the cleanest experiment is to point one of your existing CLI agents (`ww`/`zz`) at the `zenmux.ai/api/v1` base URL with a model you already benchmark, and diff latency/throughput/cost against the same model on OpenRouter for a week. Their per-channel HLE leaderboard at zenmux.ai/benchmark is also worth a look if you care about empirical channel-quality data rather than vendor claims.

**References:**

- [ZenMux](https://zenmux.ai/)
- [ZenMux Complete Guide — NxCode](https://www.nxcode.io/resources/news/zenmux-complete-guide-ai-api-gateway-2026)
- [ZenMux on Product Hunt (compensation mechanism Q&A)](https://www.producthunt.com/products/zenmux-2)
- [ZenMux GitHub org](https://github.com/ZenMux)
- [HuntifyAI — ZenMux pricing/models](https://huntifyai.com/tools/zenmux)
