---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Token Billing: Cost Proxy Rationale"
translated: false
type: note
---

Question: Why do LLM providers charge by token, when some people claim it's analogous to IBM charging by MIPS?

Answer:

The MIPS analogy is rhetorical, not technical. It's usually deployed as a *criticism* — "token billing is the new MIPS billing," meaning an artificial, rent-extracting unit decoupled from real cost. But the two are structurally different, and understanding why tells you something about LLM economics.

**Why tokens are actually a reasonable cost proxy**

Token billing works because the token is the atomic unit of compute in a transformer. The cost of serving a request is dominated by two phases, both linear (or worse) in token count:

```
Prefill:  process N_in prompt tokens   → O(N_in²) attention, O(N_in) FLOPs/layer for FFN
Decode:   generate N_out tokens        → 1 forward pass per output token
```

For a dense model, per-token compute is roughly:

```python
# FLOPs per token ≈ 2 * N_params  (forward pass, the famous 2N rule)
flops_per_token = 2 * n_params
# decode is memory-bandwidth bound, not FLOP bound:
# each output token re-reads all weights + the KV cache
```

So output tokens cost more than input tokens (that's why every provider prices `output > input`, typically 3-5x). Input tokens get batched and parallelized in prefill; output tokens are serialized and bandwidth-bound — you re-stream weights from HBM for every single token. Token count is a *real* physical correlate of GPU-seconds consumed. That's the key difference from MIPS.

**Why MIPS billing was the opposite**

IBM mainframe MIPS billing decoupled price from cost. The MIPS rating was a capacity tier baked into the *machine*, and IBM charged software licenses (and sub-capacity pricing) by it. You paid more MIPS for the *same* workload because IBM said the box was bigger — it was a price-discrimination and lock-in lever, not a usage meter. The marginal cost of running one more instruction was ~zero to IBM; the MIPS charge was pure economic rent on installed capacity.

| | MIPS (IBM) | Token (LLM) |
| --- | --- | --- |
| What it meters | Installed machine capacity tier | Actual compute consumed per request |
| Marginal cost link | Weak/none — rent on capacity | Strong — ~linear in GPU-seconds |
| Provider's marginal cost | ~0 for one more instruction | Real HBM bandwidth + FLOPs |
| Purpose | Lock-in, price discrimination | Cost pass-through (+ margin) |

**Where the critics have a point**

The analogy isn't *entirely* wrong, and here's the AI-native nuance you'd care about:

1. **Tokens aren't a fixed unit across vendors.** Different tokenizers split the same text differently. GPT's BPE, Llama's tokenizer, and DeepSeek's all produce different token counts for identical input. So "per token" isn't a stable currency — it's vendor-specific, which *is* MIPS-like (you can't trivially compare).

2. **Pricing is margin-loaded, not cost.** With MoE models (DeepSeek v4), only a fraction of params activate per token. DeepSeek v4's active-param count is far below total, so its true marginal cost per token is much lower than a dense model of equivalent total size — yet pricing doesn't always reflect that proportionally. The *flat* per-token price hides that the underlying cost structure shifted. That's where rent creeps back in.

3. **Caching breaks the linearity.** Prompt caching (Anthropic/DeepSeek/OpenAI) charges cached input tokens at ~10% of normal. This is an admission that the token isn't really the cost unit — the *uncached forward pass* is. Cached tokens skip prefill compute, so they cost almost nothing, and pricing now reflects that. The unit fractures the moment you optimize.

**The honest summary**

Token billing is a genuine usage meter, unlike MIPS — it tracks GPU-seconds with real fidelity, especially for output tokens. But it inherits *one* MIPS-like flaw: the unit is vendor-defined (tokenizer-dependent) and the price is set by margin and competition, not by transparent cost. So the claim "it's just MIPS" is half-right: same *opacity and lock-in dynamics*, completely different *physical grounding*.

If you want a cleaner cost model for your own training/inference economics, price in **GPU-seconds** directly — that's what tokens are a (lossy) proxy for, and it's the unit you actually pay AMD Dev Cloud (~$2/hr for the MI300X) in.
