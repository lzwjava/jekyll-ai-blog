---
audio: false
generated: true
image: false
lang: en
layout: post
title: Speculative Decoding Speeds Up LLMs
translated: false
type: note
---

Question: What does the YouTube video about speculative decoding explain?

Answer:
The video, titled **"Faster LLMs: Accelerate Inference with Speculative Decoding"** by IBM Technology, explains how **speculative decoding** speeds up large language model (LLM) inference (by 2–4x) without reducing output quality.

Here is a summary of the core concepts discussed in the video:

### Core Concept: Draft & Verify

Instead of relying solely on a large, slow LLM to generate text auto-regressively one token at a time, speculative decoding uses a two-model approach:

* **Draft Model (Smaller & Faster):** Quickly guesses or "speculates" a sequence of future tokens ($K$ tokens).
* **Target Model (Larger & Accurate):** Validates the draft model's guessed tokens in a single parallel step.

### The 3-Step Process

1. **Token Speculation:** The small draft model predicts $K$ tokens ahead along with their probability distributions ($DP$).
2. **Parallel Verification:** The large target model processes all $K$ tokens at once to compute its own confidence probabilities ($TP$) and predict the next single token.
3. **Rejection Sampling:** The system compares $TP$ and $DP$ token by token:
* **Accept:** If the target model agrees with or is more confident than the draft model, the token is accepted.
* **Reject & Correct:** At the first token where the target model disagrees, subsequent draft tokens are discarded, and the target model resamples the correct token.



### Benefits

* **Speedup:** Achieves 2x–3x faster inference on average (up to $K+1$ tokens generated per round).
* **Quality Retention:** Rejection sampling guarantees that output quality remains identical to running the large model alone.
* **Efficiency:** Optimizes GPU resource utilization and reduces compute costs and latency.

References:

* [Faster LLMs: Accelerate Inference with Speculative Decoding](http://www.youtube.com/watch?v=VkWlLSTdHs8)