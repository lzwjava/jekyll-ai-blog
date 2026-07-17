---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kimi K3's Low OpenRouter Ranking
translated: false
type: note
---

Question: Why is Kimi K3 (23B/large model) not ranking high on OpenRouter? Are people just using Kimi subscription instead?

Answer:

Your intuition is mostly right, but there are a few factors.

First, **Kimi K3 is not really a "cheap OpenRouter model" play**. It is positioned as a frontier model. Moonshot launched Kimi K3 as a very large open-weight model (reported 2.8T total parameters MoE, 1M context), targeting long-horizon coding/reasoning rather than cheap everyday chat. ([Reuters][1])

The OpenRouter ranking is mainly **usage volume**, not "best model". A model can be excellent but not appear high because:

1. **Price is too high for API users**

If API users compare:

* DeepSeek / Qwen style models: extremely cheap
* Kimi K3: closer to premium frontier pricing

Reported Kimi K3 API pricing is around:

```
input:  $3 / 1M tokens
output: $15 / 1M tokens
cache hit: $0.30 / 1M
```

([RouterPlex][2])

For agent loops:

```
user prompt
 -> model thinks
 -> tool call
 -> model thinks
 -> retry
 -> summarize
```

output tokens dominate. $15/M output is painful.

A lot of OpenRouter traffic is:

* coding agents
* batch generation
* hobby users
* eval scripts

They care about $/task.

---

2. **Kimi users may stay inside Kimi ecosystem**

Yes, this is a big factor.

Moonshot has:

* kimi.com
* Kimi Code
* subscription plans

The best Kimi experience is probably inside their own product because they control:

```
model
+
system prompt
+
tool calling
+
context management
+
quota
+
cache
```

Third-party API loses some of that.

Kimi Code documentation shows K3 is integrated directly with their coding environment, with special model IDs and context handling. ([Kimi][3])

So a developer who pays for Kimi subscription may never touch OpenRouter.

---

3. **OpenRouter ranking has a cold-start problem**

New models usually:

```
release
 ↓
few providers
 ↓
high price
 ↓
users try once
 ↓
traffic low
 ↓
ranking low
```

There are also reports that early OpenRouter availability was limited and providers were getting overloaded. ([Reddit][4])

---

4. The "23B" misunderstanding

If you mean **23B active parameters**, that is actually the MoE active compute number, not the total model size.

Modern MoE:

```
total params:
2.8T

per token activated:
~20-30B

```

Similar idea:

```
DeepSeek V3:
671B total
37B active
```

The important metric is:

```
quality / activated FLOPs / dollar
```

not total parameter count.

---

My current view:

Kimi K3 is probably a **technical achievement**, but the business positioning is questionable:

```
Closed frontier:
 GPT / Claude
      |
      | better UX + reliability
      |
Kimi K3
      |
      | expensive open model
      |
Cheap open models:
 DeepSeek / Qwen
```

The dangerous middle is:

* not as cheap as DeepSeek
* not as polished as Claude/OpenAI ecosystem
* too large for self-hosting

The winning strategy for open models is probably:

```
small enough to deploy
+
cheap enough to run
+
good enough for agents
```

For example:

* Qwen 30B/70B class
* DeepSeek distilled models
* future 20-50B MoE models

Kimi K3 may win if:

```
quality approaches Claude/GPT
AND
Moonshot subsidizes API cost
AND
Open weights actually become usable
```

Otherwise many users will just say:

"Interesting benchmark, but I will use DeepSeek/Qwen because my agent runs 1000 calls/day."

[1]: https://www.reuters.com/world/china/chinas-moonshot-unveils-worlds-largest-open-ai-model-closing-us-rivals-2026-07-17/?utm_source=chatgpt.com "China's Moonshot unveils world's largest open AI model, closing in on US rivals"
[2]: https://routerplex.com/blog/kimi-k3-api-pricing-setup?utm_source=chatgpt.com "Kimi K3 API: Pricing, Context Window and Setup · RouterPlex"
[3]: https://www.kimi.com/code/docs/en/kimi-code/models.html?utm_source=chatgpt.com "Model Configuration | Kimi Code Docs"
[4]: https://www.reddit.com/r/openrouter/comments/1uye4ec/kimi_k3_is_now_on_openrouter/?utm_source=chatgpt.com "Kimi K3 is now on OpenRouter"
