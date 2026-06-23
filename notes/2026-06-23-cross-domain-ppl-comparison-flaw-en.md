---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Domain PPL Comparison Flaw
translated: false
type: note
---

**Question:** What does "跨域" (cross-domain) mean in the context of comparing perplexity (PPL) across different data distributions?

**Answer:**

Your friend is making a sharp point about a common methodological flaw in LLM evaluation.

**跨域 = cross-domain comparison of PPL**

Perplexity is only meaningful *within* the same distribution. When you compute PPL on code vs. natural language, you're comparing across two fundamentally different entropy regimes — that's the "流氓行为" (sketchy/illegitimate move).

Here's why:

**Code has low entropy by design:**
- Syntax is highly constrained (keywords, brackets, indentation)
- The model has seen near-identical boilerplate billions of times
- Conditional entropy H(token | context) is tiny for most tokens
- So PPL on code is naturally low — not because the model "understands" more, but because the distribution is peakier

**Natural language has high entropy:**
- Word choice is far less constrained
- Human writing is diverse, idiomatic, context-dependent
- The distribution is flatter → higher PPL by construction

**The flaw:** If model A gets PPL=5 on code and PPL=15 on prose, you *cannot* say "model A is 3x better at code than prose." The scales aren't comparable. PPL=5 on code might represent *worse* relative modeling than PPL=15 on prose, because the baseline entropy of code is so much lower.

**Mathematically:**

```
PPL = exp(H(p, q))  # cross-entropy between true dist p and model q
```

If `H(p_code)` ≈ 2 bits and `H(p_prose)` ≈ 8 bits, then a perfect model would get PPL≈4 on code and PPL≈256 on prose. Comparing raw PPL numbers across these is apples-to-oranges.

**The right comparison** would be something like:
- PPL relative to an oracle/ground-truth language model on the same domain
- Or bits-per-character normalized by domain entropy
- Or just: eval on the *same* held-out test set for both models

Your friend is essentially calling out "my model gets lower PPL" claims that cherry-pick easy domains (code, structured data) to make numbers look good.
