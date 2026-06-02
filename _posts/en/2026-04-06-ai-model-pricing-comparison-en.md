---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Model Pricing Comparison Misunderstanding
translated: false
type: note
---

Question: why xiaomi mimo often cheap than minimax m2.7 though minimax m2.7 show more expensive in million token input and output

Answer: Based on current pricing data and model specifications, there is a misunderstanding regarding which model is more expensive. **MiniMax-M2.7 is actually significantly cheaper per million tokens than Xiaomi MiMo-V2-Pro.** The discrepancy in "perceived" cost versus "actual" cost likely stems from how each model handles **reasoning tokens** and their respective pricing tiers on platforms like OpenRouter.

### 1. Pricing Comparison (Per 1 Million Tokens)

| Model | Input Price | Output Price | Context Window |
| :--- | :--- | :--- | :--- |
| **MiniMax-M2.7** | ~$0.30 | ~$1.20 | 204,800 |
| **Xiaomi MiMo-V2-Pro** | $1.00 | $3.00 | 1,048,576 |

As shown above, Xiaomi's MiMo-V2-Pro is roughly **3.3x more expensive for input** and **2.5x more expensive for output** than MiniMax-M2.7.

### 2. The Role of Reasoning Tokens

You mentioned that MiniMax might be more expensive due to a `/think` or reasoning mechanism. Here is how that affects the total cost:

* **Reasoning-Heavy Models:** MiniMax-M2.7 is a "reasoning-only" or reasoning-optimized model. While its *price per token* is lower, it generates a much higher volume of hidden **internal reasoning tokens** (the "thinking" process) before providing a final answer.
* **Token Efficiency:** Even though MiniMax-M2.7 uses ~55% more output tokens than its predecessor (M2.5) to "think" through a problem, it remains more token-efficient than other reasoning models like GLM-5.
* **Xiaomi's Approach:** Xiaomi MiMo-V2-Pro also has a **Reasoning Mode**, but it typically uses fewer tokens to reach an answer compared to MiniMax. However, because its base price is so much higher ($3.00 vs $1.20), the "cheaper" total for Xiaomi only happens on very short, simple tasks where reasoning is minimal.

### 3. Summary of Cost Differences

* **Why MiniMax seems "more expensive" in practice:** If you use MiniMax for a complex task, it might generate 2,000 "thinking" tokens to give you a 100-token answer. You are billed for all 2,100 tokens.
* **Why Xiaomi is objectively more expensive:** For any fixed amount of data (e.g., a 10,000-word document), Xiaomi will always cost more to process because its base rate per token is higher.
* **The Context Factor:** Xiaomi offers a much larger **1-million token context window**, which requires more expensive hardware to maintain, contributing to its higher $1/$3 price point.

References:

* [MiniMax M2.7 - API Pricing & Providers - OpenRouter](https://openrouter.ai/minimax/minimax-m2.7)
* [Xiaomi: MiMo-V2-Pro – Provider Status and Pricing | OpenRouter](https://openrouter.ai/xiaomi/mimo-v2-pro/providers)
* [MiniMax M2.7 vs MiMo v2 Pro - Pricing & Benchmark Comparison 2026](https://pricepertoken.com/compare/minimax-minimax-m2.7-vs-xiaomi-mimo-v2-pro)
