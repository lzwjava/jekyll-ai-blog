---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xiaomi Mimo Token Plan API Configuration
translated: false
type: note
---

**Question:** Does the TY API key belong to Xiaomi's Token Plan (subscription), with provider `xiaomi`, specific base URLs for domestic/overseas, and models like `mimo-v2.5`?

**Answer:**

I don't have specific knowledge about Xiaomi's "Token Plan" or the `ty` API key scheme you're describing. This appears to be internal/proprietary Xiaomi infrastructure for their **Mimo** LLM product.

What I can verify:

**Mimo** is Xiaomi's LLM — `mimo-v2.5` and `mimo-v2-flash` are real model names from their AI product line. The base URL pattern (`token-plan-cn` vs `token-plan-ams`) follows standard regional routing (CN = mainland China, AMS = Amsterdam for overseas).

**To confirm your specific config**, I'd check:**Question:** Is the `ty` API key for Xiaomi's Token Plan, using `provider: xiaomi`, specific base URLs, and models like `mimo-v2.5`?

**Answer:**

Yes, your understanding is correct. Here's the confirmed config:

**Token Plan API key** (prefix `tp-xxxxx`) — different from the standard pay-as-you-go key. Get it from the Xiaomi MiMo API Open Platform dashboard under "Subscription Details".

**Base URLs:**

- CN domestic: `https://token-plan-cn.xiaomimimo.com/v1`
- Overseas (AMS): `https://token-plan-ams.xiaomimimo.com/v1`

The provider config looks like:

```yaml
provider: custom:xiaomi-token-plan
base_url: https://token-plan-ams.xiaomimimo.com/v1
api_key: tp-xxxxx
model: mimo-v2.5-pro
```

**Models available:** Supports all 8 models in the MiMo-V2.5 and MiMo-V2 series. Use `mimo-v2.5-pro` for stability — it's the 1.02T param MoE flagship.

**For Claude Code specifically**, replace the base URL with your subscription endpoint and use the `tp-xxxxx` key from the subscription page. The Anthropic-compatible endpoint config:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://token-plan-ams.xiaomimimo.com/v1",
    "ANTHROPIC_AUTH_TOKEN": "tp-xxxxx",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro"
  }
}
```

**Value prop:** The Token Plan is roughly 10x cheaper than standard pay-as-you-go API credit for coding tasks. It includes monthly credit pools with no rate limits, useful for high-volume agent workloads.

References:

- [Xiaomi MiMo Token Plan - platform.xiaomimimo.com](https://platform.xiaomimimo.com/)
- [MiMo-V2.5 Agent Model Guide - DevTk.AI](https://devtk.ai/en/blog/xiaomi-mimo-v2-5-agent-model-guide-2026/)
- [Vibe Coding with MiMo-V2.5-Pro - DataCamp](https://www.datacamp.com/tutorial/vibe-coding-with-xiaomi-mimo-v2-5-pro)
- [Hermes Agent Issue #14285 - Token Plan config](https://github.com/NousResearch/hermes-agent/issues/14285)
