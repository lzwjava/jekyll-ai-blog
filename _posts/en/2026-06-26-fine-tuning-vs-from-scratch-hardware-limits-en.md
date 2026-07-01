---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Fine-Tuning vs. From-Scratch: Hardware Limits"
translated: false
type: note
---

**Question:** Is fine-tuning DeepSeek v4 or GLM 5.2 on finance data a good idea — compared to or instead of the from-scratch GPT-2 SEC model?

Let me check current specs on both before answering, since these are recent models and the sizing determines whether this is even feasible on your hardware.I have enough to answer. The sizing alone settles most of the question.

**Question:** Is fine-tuning DeepSeek V4 or GLM 5.2 on finance data a good idea — instead of, or alongside, the from-scratch GPT-2 SEC model?

**Answer:**

Mostly no — at least not the way the question frames it. Let me be direct, because the sizing makes this concrete rather than "it depends."

**The hardware wall is the first answer**

DeepSeek V4 ships in two open-weight sizes: V4-Pro at 1.6T total / 49B active, and V4-Flash at 284B total / 13B active. Both are MoE transformers under MIT license. Your hardware:

- 4070 12GB — can't even *hold* V4-Flash's 284B weights, let alone train. Inference of the full model needs offloading; full-parameter fine-tuning is out of the question by 2+ orders of magnitude.
- MI300X 192GB — can run V4-Flash inference comfortably, but **full fine-tuning a 284B MoE needs optimizer states + gradients + activations**, which at even 8-bit is well past 192GB. You'd need a multi-node cluster. V4-Pro at 1.6T isn't in the conversation on any hardware you have.

So "fine-tune DeepSeek V4" really means one of two narrower things, and you should name which:

1. **LoRA / QLoRA on V4-Flash** — adapter-only, freeze the base, train a few hundred million adapter params. *This* fits on the MI300X. Full fine-tune does not.
2. **LoRA on a small dense model** (Qwen3-4B/8B, Llama-3.x-8B) — trivially fits the 4070, fast iteration.

GLM 5.2 — I'd want to confirm its exact open-weight sizes before committing (the GLM line has historically shipped 9B/32B-class dense plus larger MoE variants), but the same logic applies: dense ≤32B is LoRA-able on the MI300X, anything bigger is adapter-only or out.

**The deeper question: does fine-tuning even buy you what GPT-2-from-scratch did?**

These are two different exercises with different payoffs, and you should be clear-eyed about what each demonstrates:

| | GPT-2 124M from scratch (what you did) | LoRA on V4-Flash / GLM |
|---|---|---|
| What it proves | You own the full pretraining pipeline | You can adapt a frontier base |
| Learning value | High — tokenizer→data→training loop→optimizer, all yours | Medium — mostly data prep + PEFT config |
| Output quality | Plausible SEC text, no reasoning | Frontier reasoning + finance flavor |
| Hardware | Single 4070, 9h | MI300X, adapter-only |
| Internal "wow" at bank | "built a model" | "made the good model better at our domain" |

Here's the thing that matters for your trajectory: **the from-scratch run is the more impressive capability and the rarer skill**, but the LoRA fine-tune is the more *useful artifact* in a bank. Most engineers can't train from scratch; almost no one needs to. Everyone wants a domain-adapted frontier model.

**Does finance fine-tuning actually help? Mostly only if you have instruction data, not raw text**

Critical distinction your SEC dataset surfaces: you have **1.55B tokens of raw 10-K text**. That's a *continued-pretraining* corpus, not a fine-tuning corpus.

- **LoRA on raw SEC text** (continued pretraining) on a frontier model gives you *very little*. V4-Flash has already seen enormous amounts of financial filings in pretraining. Pushing more raw 10-K text through a low-rank adapter mostly teaches it stylistic boilerplate it already knows. Low ROI.
- **LoRA on instruction/task pairs** (e.g. "extract the risk factors from this filing → structured JSON", "summarize this MD&A", "answer this question about this 10-K") is where fine-tuning a frontier base actually moves the needle. But you don't have this dataset yet — you'd have to *build* it, likely by using V4-Pro/Opus to generate the labels from your raw filings.

So the real AI-native play isn't "fine-tune V4 on finance." It's: **use a frontier model to distill an instruction dataset from your SEC corpus, then LoRA a small model on it** — a distillation pipeline. That's the thing worth building, and it's genuinely useful + demonstrable + fits your hardware.

**What I'd actually do, in order**

1. **Ship the GPT-2 run first** (you're nearly done) — it's your strongest "I own the full stack" artifact. Don't dilute it by pivoting before it lands.

2. **For the next project, do the distillation play, not raw fine-tuning:**
   - Take a few thousand 10-K sections from your corpus.
   - Use V4-Pro or Opus via API to generate task pairs (QA, extraction, summarization) — you already consume 3B tokens/yr, this is cheap.
   - LoRA a Qwen3-8B or Llama-3.1-8B on the 4070 first (fast iteration), then scale to V4-Flash LoRA on the MI300X if the small one shows signal.
   - **This gives you a real eval**: held-out task accuracy, not perplexity. Far more persuasive internally than either a loss curve or "it sounds like a 10-K."

3. **Benchmark against the obvious baseline**: zero-shot V4-Flash vs. your LoRA'd V4-Flash on the held-out tasks. If the adapter doesn't beat zero-shot, you've learned something cheap and important (that the base already covers finance well). If it does, you have a deployable artifact.

**Bottom line:** Full fine-tuning V4-Pro/Flash is hardware-infeasible for you; LoRA on V4-Flash fits the MI300X but raw-text continued pretraining on it is low-ROI. The high-leverage version is a *distillation → LoRA on a small/mid model* pipeline driven by frontier-model-generated instruction data. That advances your actual goals (agent/distillation/eval skills) far more than pushing 10-K text through an adapter, and it produces a downstream-task benchmark that lands much harder in the bank than another loss number.

One scoping question before you build, since it changes the dataset design entirely:
