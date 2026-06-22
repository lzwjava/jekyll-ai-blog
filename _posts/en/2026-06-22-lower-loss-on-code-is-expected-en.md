---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lower Loss on Code Is Expected
translated: false
type: note
---

Current state at iter 70,700 / 427,000 (16.6%):

    Step 70,000 checkpoint:
      train loss: 2.1042
      val loss:   2.0817   (best so far, down from 5.87 at iter 14k)

    Speed: 621ms/step, MFU ~14.4%
    ETA: ~62 hours (~2.5 days) remaining

You're right — the loss is much lower than fineweb-edu text. That's expected, not a bug:

Code is inherently more predictable than natural language:
  - Rigid syntax (boilerplate, imports, braces, indentation)
  - Repeated patterns (function signatures, decorators, for-loops)
  - Smaller effective vocabulary
  - Whitespace/indentation is highly predictable

For comparison:
  GPT-2 124M on WebText (natural text): ~2.85 val loss
  GPT-2 124M on FineWeb-Edu:            ~3.0-3.2 val loss
  This run on GitHub code:              ~2.08 val loss

The lower loss doesn't mean "better model" — it means code has lower per-token entropy. The model is learning well and loss is still decreasing. It should bottom out around 1.8-1.9 by the end of training.
