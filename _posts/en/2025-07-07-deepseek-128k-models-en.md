---
audio: false
generated: true
lang: en
layout: post
title: DeepSeek's 128K Token Models in 2025
translated: false
type: note
---

As of June 2025, DeepSeek has a range of models with impressive context lengths, often leveraging their Mixture-of-Experts (MoE) architecture for efficiency. Here's a breakdown:

* **DeepSeek-R1:** This model, released in January 2025, is noted for supporting a context length of **128,000 tokens** (or 131,072 tokens in some benchmarks). It's particularly strong in math, coding, and structured thinking due to its Reinforcement Learning (RL) post-training.
* **DeepSeek-V3:** Released in December 2024, DeepSeek-V3, including its base model, also supports a context length of **128,000 tokens**. It's a powerful MoE model with 671 billion total parameters (37 billion active per query).
* **DeepSeek-Coder-V2:** This code-focused MoE model, released in July 2024, has a significant context window of **128,000 tokens**. It supports a wide range of programming languages (338).
* **DeepSeek-V2:** Launched in May 2024, DeepSeek-V2 boasts a context length of **128,000 tokens**. This MoE model aims for economical training and efficient inference.
* **DeepSeek-V2.5:** Released in September 2024, this model combines general and coding capabilities and also supports a **128,000 token** context window.

**Important Considerations:**

* **Native Context Length vs. API Limits:** While some DeepSeek models have a native context length of up to 163,840 tokens, the DeepSeek API may limit the available context window for specific models (e.g., "deepseek-chat" and "deepseek-reasoner" currently have a 64K context limit through their API). If you need the full context, running the models locally or using API providers that allow longer contexts might be necessary.
* **Performance Degradation:** Similar to other large language models, while models might advertise very long context windows, performance (accuracy, reasoning) can sometimes degrade when pushed to the absolute maximum length. DeepSeek R2, for example, is expected to address the 15% performance drop observed in R1 at its maximum 128,000-token context window.

In summary, DeepSeek is a strong player in the long-context LLM space, with several models in June 2025 offering a 128K token context window, making them suitable for handling extensive inputs and complex tasks.
