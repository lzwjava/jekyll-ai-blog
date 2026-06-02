---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: DeepSeek Token Pricing Details Explained
translated: false
type: note
---

To directly address your observation: DeepSeek v3.2 did announce a significant price drop—up to 50% or more in some cases—but the actual cost reduction users experience can vary due to several factors:

- **Headline Price vs. Effective Cost:** DeepSeek announced a price cut from $1.68 to $0.42 per million tokens (a 75% decrease in some contexts), but this is for raw token pricing. Your actual costs depend on your specific usage pattern: input vs. output token ratio, cache hit/miss rates, and whether you’re using off-peak discounts (which can be as high as 50–75% off during certain hours) ue202turn0search1,[1],[2].
- **Cache Efficiency:** If your workload benefits from caching (e.g., repeated prompts or context reuse), the effective cost may be lower than the headline price suggests, but the advertised price drop only applies to the base rate, not necessarily to cached tokens.
- **Input/Output Asymmetry:** Some models charge different rates for input and output tokens. If the price drop only applies to input tokens but your task is output-heavy, the overall cost reduction will be less than 50%.
- **Off-Peak Discounts:** DeepSeek offers additional discounts during off-peak hours (16:30–00:30 UTC), which can further reduce costs if your usage aligns with these times ue202turn0search2.

**Why you didn’t see an immediate 50% cost drop:**
- The price drop may not have been applied uniformly across all token types or usage scenarios.
- Your task’s specific token distribution (input/output, cache hit/miss) may not align with the advertised price reduction.
- There can be a delay between the announcement and the price change being reflected in all billing systems or APIs.

In summary, while DeepSeek v3.2’s price drop is real and substantial, the actual cost savings depend on your usage pattern and may not match the headline percentage exactly ue202turn0search1,[1],[2].

Citations:
[1] https://x.com/deepseek_ai
[2] https://www.facebook.com/groups/developerkaki/posts/2615893198756577/
