---
audio: false
generated: true
image: false
lang: en
layout: post
title: Speeding Up Large Language Models
translated: false
type: note
---

**Speculative decoding** is a technique for making large language models generate text **faster without changing the output distribution**.

The basic idea is: **a small, fast model guesses several tokens ahead, and a larger model checks those guesses in parallel.**

Suppose the model is generating:

> “The capital of France is …”

Normally, a large model generates sequentially:

**Paris → is → known → for → …**

Each token requires another expensive forward pass.

With speculative decoding:

1. A **draft model** (small and fast) proposes several tokens, e.g. `Paris is known for`.
2. The **target model** (large and slow) evaluates those proposed tokens **in one forward pass**.
3. It accepts as many of the guesses as are valid under its own probability distribution.
4. Once a guess is rejected, generation is corrected according to the target model, and the process repeats.

So instead of getting roughly **1 token per expensive large-model pass**, you might get **several accepted tokens per pass**.

### Why it's interesting

The clever part is that properly implemented speculative decoding isn't simply saying *"trust the smaller model when it looks right."* The acceptance/rejection procedure is constructed so that the resulting tokens have **the same statistical distribution as if the large model had generated them normally**.

In simplified terms:

**Normal decoding**
`Large → token → Large → token → Large → token`

**Speculative decoding**
`Small → 5 guesses → Large checks all 5 → accepts perhaps 4 → repeat`

That can substantially reduce **generation latency**, especially when the draft model predicts the large model well.

The main tradeoff is that if the draft model makes poor predictions, many proposed tokens get rejected, so the speedup shrinks. This is why a good draft model needs to be **cheap but strongly aligned with the target model's predictions**.

If you want, I can also explain the **math behind the acceptance/rejection step**, which is the particularly clever part of speculative decoding.