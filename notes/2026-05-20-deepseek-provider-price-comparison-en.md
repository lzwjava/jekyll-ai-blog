---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek Provider Price Comparison
translated: false
type: note
---

Good catch. The prices I cited ($1.74 input / $3.48 output) came from the search results — likely reflecting DeepSeek's **official API** pricing at platform.deepseek.com.

OpenRouter's prices are different because **OpenRouter is a reseller/aggregator** — they route across multiple providers and their pricing reflects their own margins plus whatever provider they route to. Sometimes OpenRouter is cheaper than the official API, sometimes more expensive, depending on which backend provider wins the routing.

In this case:

| Source | Input $/M | Output $/M |
|---|---|---|
| DeepSeek official API | $1.74 | $3.48 |
| OpenRouter | $0.435 | $0.87 |

OpenRouter is actually **4x cheaper** than DeepSeek's own API for V4 Pro. That's likely because OpenRouter routes to providers (e.g. Fireworks, Together, Nebius) who are running the open weights themselves and competing on price.

This is the value prop of OpenRouter for open-weight models — the MIT license means anyone can host it, and competition between providers drives prices down significantly below the lab's own API price.

So the corrected practical numbers for your routing decisions: **$0.435/M input, $0.87/M output** on OpenRouter for V4 Pro, and $0.112/$0.224 for V4 Flash. That makes V4 Flash even more of a no-brainer for high-volume agent loops.
