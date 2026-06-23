---
audio: false
generated: true
image: false
lang: en
layout: post
title: Low PPL Meaning in LLM Training
translated: false
type: note
---

**Question:** What does low PPL (perplexity) mean in LLM training, and why does it matter?

**Answer:**

Perplexity is just exponentiated cross-entropy loss:

```
PPL = exp(L) = exp( -1/N * Σ log P(x_i | x_<i) )
```

So **low PPL = model assigns high probability to the actual next tokens = better fit to the data**.

---

## The Math

Cross-entropy loss per token:

```
L = -1/N * Σ_{i=1}^{N} log P_θ(x_i | x_1, ..., x_{i-1})
```

PPL = `exp(L)`. If PPL = 10, the model is as "confused" as if it had to pick uniformly from 10 equally likely tokens at each step.

- PPL = 1 → perfect prediction (overfit or data leaked)
- PPL = vocab\_size → random model
- GPT-2 on WikiText-103 → ~18–20
- GPT-4 class models → single digits on clean text

---

## In Training Context

```python
# nanoGPT style
loss = F.cross_entropy(logits.view(-1, vocab_size), targets.view(-1))
ppl = torch.exp(loss)  # that's it
```

Low PPL during training means:

1. **Model is learning the data distribution** — good
2. **If val PPL >> train PPL** → overfitting
3. **If PPL stops decreasing** → LR too low, data exhausted, or architecture bottleneck

---

## Code Perplexity Specifically

You asked about **code PPL**. Code has different characteristics vs natural language:

- Higher entropy in identifiers (variable names, function names)
- But low entropy in syntax (keywords, brackets, semicolons)
- Good code models reach PPL ~2–5 on syntax tokens but higher on semantic tokens

For CodeLlama/DeepSeek-Coder, they evaluate on HumanEval pass@k rather than PPL alone — because low PPL doesn't always mean good code generation.

---

## Practical Interpretation During Your Training Runs

| PPL Range | What it means |
|-----------|--------------|
| Dropping fast early | Normal — model learning basic patterns |
| Plateau | LR decay needed, or data quality issue |
| Val PPL rising while train PPL drops | Overfitting |
| Sudden spike | Gradient explosion, bad batch, NaN |
| Very low (< 2 on train) | Possible data contamination or memorization |

In nanoGPT you'll see this logged as both `loss` and optionally `ppl = exp(loss)`. They're identical information, just different scales. Loss is more useful for gradient math; PPL is more interpretable as "how many choices is the model confused between."
