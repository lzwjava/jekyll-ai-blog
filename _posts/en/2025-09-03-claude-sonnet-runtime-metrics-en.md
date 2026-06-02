---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Sonnet Runtime Metrics Explained
translated: false
type: note
---

What you’re seeing are **runtime metrics** from the inference of `anthropic/claude-sonnet-4` through Google Vertex AI. Let me break it down:

* **First token latency (2.85s):**
  This is the delay between sending your prompt and receiving the very first output token. It includes network latency, request queuing, and the model’s initial computation. For large models like Claude Sonnet, a couple of seconds is normal.

* **Throughput (32.9 tokens/sec):**
  After the first token is generated, the model streams subsequent tokens. 32.9 tokens per second is a healthy rate — not the fastest possible, but good for a large model. Throughput can vary depending on model size, load on the provider (Vertex), and your prompt length.

* **Finish reason (stop):**
  This simply indicates that the model stopped naturally when it reached the end of its generated text (as opposed to hitting a length limit, cutoff, or error).

So, **“why?”** → because these numbers describe normal inference characteristics of a large LLM when run through Vertex:

* Some startup latency is expected (compilation, optimization, routing).
* Throughput stabilizes once generation begins.
* Stop is the intended completion condition.

Do you want me to also compare these numbers with typical performance ranges for other models (like GPT-5, Gemini Pro, DeepSeek, etc.) so you can see if this was “fast” or “slow” in context?
