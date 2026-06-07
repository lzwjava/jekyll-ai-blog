---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transformer context window prediction explanation
translated: false
type: note
---

Question: In a Transformer with a context size of 1024, are 1023 tokens used to predict the 1024th token, or are 1024 tokens used to predict a new token outside that window?

Answer: You are correct that it is the latter. In a Transformer model (like GPT), if the maximum context window is **1024**, the model can take up to **1024 tokens as input** to predict the very next token (the 1025th).

Here is a breakdown of how that space is utilized:

### 1. The Context Window Limit

The "context size" refers to the maximum number of tokens the model can "see" or attend to at once. If your limit is 1024, the model creates an attention matrix of $1024 \times 1024$.

### 2. Training vs. Inference

* **During Training:** The model is actually processing all 1024 tokens simultaneously. Because of **causal masking** (also called look-ahead masking), the model is trained so that:
* Position 1 predicts token 2.
* Position 2 (seeing 1 and 2) predicts token 3.
* ...
* Position 1024 (seeing tokens 1 through 1024) predicts token **1025**.

* **During Inference (Generation):** If you provide a prompt of 1024 tokens, the model uses the hidden state of that 1024th token to generate the next one. Once that new token is generated, the window must "slide" or start dropping the oldest tokens because it cannot exceed its hard limit of 1024.

### 3. Summary of Input/Output

| Input Size | Role | Output |
| --- | --- | --- |
| **1023 tokens** | Predicting the end of the window | Token 1024 |
| **1024 tokens** | Maxing out the context | Token 1025 |

So, if you have a full 1024-token buffer, the model uses all 1024 of them to decide what the next single token should be. It doesn't "save" a slot in the context window for the prediction; the prediction is a probability distribution over the vocabulary generated *from* the existing context.
