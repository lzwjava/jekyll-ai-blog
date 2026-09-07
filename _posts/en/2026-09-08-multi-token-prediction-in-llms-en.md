---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Token Prediction in LLMs
translated: false
type: note
---

Question: What does **MTP** mean in LLMs?

Answer: In modern LLM inference, **MTP usually means *Multi-Token Prediction***.

Instead of the normal autoregressive model predicting only the next token:

```text
x1 x2 x3 x4 → predict x5
```

MTP trains the model to predict **multiple future tokens simultaneously**:

```text
x1 x2 x3 x4 → predict x5, x6, x7, ...
```

### Why it matters

The main use is **speculative-style decoding / faster inference**.

A normal decoder does:

```text
forward()
  → token 101

forward(token 101)
  → token 102

forward(token 102)
  → token 103
```

Each token requires another expensive forward pass.

With MTP:

```text
                 ┌→ token 101
forward() ───────┼→ token 102
                 ├→ token 103
                 └→ token 104
```

The extra prediction heads can propose several tokens, and the main model verifies them.

So potentially:

```text
Normal:
1 forward → 1 accepted token

MTP:
1 main forward → several proposed tokens
                ↓
          verify them
                ↓
       accept 2–4 tokens
```

This can substantially increase **tokens/sec**, especially for workloads where consecutive tokens are relatively predictable, such as code.

### Example: DeepSeek

This is particularly associated with **DeepSeek's MTP architecture**. DeepSeek describes MTP as predicting multiple future tokens during training, with the additional prediction modules also usable for speculative decoding during inference.

Conceptually:

```text
                 hidden state
                      │
             ┌────────┴────────┐
             ↓                 ↓
        normal head        MTP module 1
             ↓                 ↓
           t+1               t+2
                               │
                         MTP module 2
                               ↓
                              t+3
```

The important distinction is:

**MTP ≠ simply generating multiple tokens independently.**

The predictions are trained to correspond to **future positions in the same sequence**, and the architecture can use them to improve decoding efficiency.

If you're looking at **DeepSeek-V3/R1 or a specific inference engine like vLLM**, MTP has some additional implementation details around KV cache and speculative decoding. I can walk through the actual forward pass and tensor shapes.