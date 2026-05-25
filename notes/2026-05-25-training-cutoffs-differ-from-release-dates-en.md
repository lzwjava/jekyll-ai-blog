---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Cutoffs Differ from Release Dates
translated: false
type: note
---

**Question:** DeepSeek-V2-Lite-Chat says GPT-4 hasn't been officially released — what does this tell us about its actual training cutoff?

**Answer:**

This is a much cleaner signal than the date hallucination. Let's bracket it properly.

## What we now know

| Event | Actual Date | Model knows it? |
|-------|-------------|-----------------|
| GPT-4 release | March 14, 2023 | ❌ No |
| GPT-4o release | May 13, 2024 | ❌ No (didn't even parse the question right) |
| DeepSeek-V2 release | May 2024 | — |

The model said GPT-4 "has not been officially released" — meaning its training data cuts off **before March 2023**.

## This is surprising for V2-Lite

DeepSeek-V2 was released in May 2024. You'd expect a mid-2024 cutoff. But the Lite variant specifically — it's possible:

1. **Base pretraining cutoff is earlier than the release date** — DeepSeek likely pretrained the base model on data through late 2022/early 2023, then spent months on MoE architecture work, SFT, RLHF, and alignment before the May 2024 release
2. **The SFT/chat fine-tuning data is from an older snapshot** — the `-Chat` suffix means it went through instruction tuning, but that tuning data may itself have a 2022 cutoff
3. **Lite vs full V2** — the Lite variant may have used an older or smaller pretraining corpus compared to the full V2

## The September 22, 2022 date wasn't a total hallucination

Given this new evidence, that date is actually plausible as a rough anchor for where the training data density peaks. The model has seen lots of text through late 2022, very little after that.

**Revised estimate: training data cutoff ≈ late 2022 (Oct–Dec 2022)**

## Cross-check with one more probe

```
You: Do you know about ChatGPT?
```

ChatGPT launched November 30, 2022. If it knows ChatGPT → cutoff is post-Nov 2022. If it doesn't → pre-Nov 2022. That would pin it within a 1-2 month window.

## The broader lesson

For any open-weight model you run locally, the release date ≠ training cutoff. The pipeline is typically:

```
pretraining data cutoff
    → months of training on GPUs
        → SFT / RLHF / DPO
            → evaluation + safety
                → public release
```

That gap is often **6–18 months** for large models. DeepSeek-V2-Lite appears to be on the longer end of that gap, or was pretrained on a deliberately older corpus to save compute on data processing.