---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Small Models Need Full Prompts
translated: false
type: note
---

Question: For small models specifically — ChatGPT and the industry may have other post-training methods, or the problem may resolve as models scale. But for a 124M small model, whether text or code, you need to feed a full prompt paragraph to get decent output. Is that right?

Answer:

Yes, your observation is correct, and there's a concrete mechanistic reason for it. Let me go one layer deeper than "small models are dumb."

## Why 124M models need the full paragraph

A 124M model (GPT-2 small: 12 layers, 768 hidden, 12 heads) has very limited capacity to **store priors**. Large models compress enormous amounts of world knowledge and task structure into weights, so a terse prompt ("fix this bug") activates rich latent task representations. A 124M model simply hasn't memorized those task→behavior mappings. So it relies almost entirely on **in-context information** rather than parametric knowledge.

In transformer terms: the model's output distribution is

```
P(next | context) = softmax(W_unembed · h_L)
```

where `h_L` is the final-layer residual stream. For a big model, `h_L` carries strong task-conditioning even from a short context because attention heads and MLPs have learned to "fill in" the implied task. For 124M, the residual stream is mostly driven by what's literally in the tokens — there's no rich prior to interpolate from. **Short prompt = thin residual = generic continuation.**

This is why few-shot and verbose prompting works disproportionately well at small scale: you're externally supplying the conditioning the weights can't.

## The scaling part of your claim

Two things resolve it as you scale, and they're separable:

1. **Pretraining scale** — emergence of in-context learning. ICL ability scales sharply; below ~1B params, few-shot gains are weak and erratic. This is the Kaplan/Wei "emergent abilities" regime. Your 124M is below the knee of that curve.

2. **Post-training (the part you're asking about)** — SFT + RLHF/DPO is what turns "needs a paragraph" into "follows a 3-word instruction." Instruction tuning literally trains the model to map terse instructions to behaviors. But — critically — **instruction tuning a 124M model gives much smaller returns** because the model lacks the base capabilities to be elicited. You can't RLHF competence the model never learned in pretraining. InstructGPT showed alignment recovers/redirects existing capability; it doesn't create it.

So your intuition splits cleanly:

- "Industry has other post-training methods" → true, but they mostly help models that already have latent capability.
- "Gets solved as models grow" → true, and it's the dominant factor for a 124M model. No post-training trick fully substitutes for scale here.

## Practical implication for your nanoGPT/nanochat work

For a 124M model, your highest-leverage moves are, in order:

1. **Domain-narrow it.** A 124M model that does *one* thing (e.g. only Python completion) is far better than a generalist 124M. Restrict the pretraining/finetune distribution.
2. **Heavy SFT with explicit instruction→output pairs**, formatted exactly as you'll prompt at inference. Small models are extremely format-sensitive — the prompt template *is* part of the task representation. Train-time and test-time formatting mismatch destroys small-model performance disproportionately.
3. **Keep prompts verbose and few-shot at inference.** This is the right call, not a failure — you're compensating for missing parametric priors with context. Don't fight it.
4. **Consider distillation** from a large model (logit/sequence-level KD) — for a fixed 124M budget, distilled models beat from-scratch SFT because the targets carry the large model's task conditioning.

The one-line summary: at 124M, behavior is **context-dominated, not weight-dominated**, so verbose prompts aren't a workaround — they're the operating regime. Post-training helps, scale helps more, and the cheapest path to "terse prompts work" is narrowing the task domain rather than improving the prompting.

References:

- [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)
- [Training language models to follow instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
- [Emergent Abilities of Large Language Models](https://arxiv.org/abs/2206.07682)
- [Scaling Laws for Neural Language Models (Kaplan et al.)](https://arxiv.org/abs/2001.08361)
- [Distilling the Knowledge in a Neural Network (Hinton et al.)](https://arxiv.org/abs/1503.02531)
