---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Model Training Data Mix Diagnosis
translated: false
type: note
---

**Question:** Is it right that you can't train a code model on just code — should it be a mixture like 20% code, 80% something else? And what do I make of this training diagnosis?

**Answer:**

Two separate questions here. Let me take them in order.

### 1. "Can't train with just code, should be code 20%?"

You *can* train on pure code — CodeParrot, StarCoder-base, the original Codex were trained on essentially 100% code and worked fine. So the "you must mix in natural language" claim is **not a hard rule**. But there's a real signal underneath your intuition:

- **Code-only models** (CodeParrot, SantaCoder, StarCoderBase) → near 100% code, good at completion, weak at following instructions or explaining.
- **Code-capable general models** (DeepSeek-Coder-V2, Qwen2.5-Coder, Llama, GPT) → deliberately mix. The exact ratios from papers:
  - **DeepSeek-Coder-V2**: pretrained on ~60% code, 10% math, 30% natural language.
  - **DeepSeek-Coder (v1)**: 87% code, 10% English NL related to code (markdown, StackExchange), 3% Chinese NL.
  - **StarCoder2 / The Stack v2**: code-heavy but with pull requests, issues, notebooks, docs — i.e. code *plus* the natural language surrounding code.

So the mix isn't "20% code." It's usually the opposite — **code-dominant with a NL slice (10–40%)**. The NL helps with: comments, docstrings, variable naming semantics, and reasoning. Why does it help even for pure code generation? Because code is full of natural language (identifiers, comments, strings), and NL pretraining gives the model better priors over those tokens than seeing them only in code context.

For your 124M nanoGPT-scale model, the mix is **not your problem**. Don't add NL yet. Your problem is data quality, which the diagnosis nails.

### 2. The diagnosis — is it right?

Mostly yes, with one important correction.

**What's correct:**

- **Dirty data is the real culprit.** `codeparrot/github-code` is a raw dump. License headers, HTML javadoc, config stubs — all true. This is exactly why BigCode built The Stack with aggressive filtering and why every serious code model deduplicates heavily. Dedup alone gave measurable gains in the StarCoder work.
- **The reference losses are roughly right.** GPT-2 124M on OWT lands ~2.85–2.9. CodeParrot-small ~3.0. Your 3.47 is genuinely high, meaning the model is leaving a lot on the table.
- **Option A/B (clean or swap data) is the highest-impact fix.** Correct. The Stack v2 (`bigcode/the-stack-v2`) or even `bigcode/the-stack-dedup` will outperform raw github-code at the same compute.

**What's wrong or misleading:**

**The "space token domination" framing is mostly a non-problem.** 26% spaces is *normal* for code — indentation is real structure, not noise. GPT-2's BPE tokenizer is also notoriously bad at code precisely because it shreds whitespace into many single-space tokens; that's a *tokenizer* issue, not a data issue. The model predicting 46.8% space after `def quicksort(arr):` isn't pathological — a newline-then-indent is genuinely the most likely continuation. So I'd discount this point. **If you want a real lever here, switch to a code-aware tokenizer** (StarCoder's tokenizer handles whitespace with dedicated tokens for runs of spaces/tabs), which alone improves effective context and loss.

**"Underfitting not overfitting" — train loss > val loss is a red flag worth checking before you trust it.** For a from-scratch 124M run, train loss being *higher* than val loss usually means one of:
- val set is easier/less diverse than train (small or non-representative val split — very common with a tiny held-out slice of one dataset),
- you're measuring train loss *with* dropout active but val *without* it (dropout inflates train loss),
- LR is still too high / you stopped on a noisy estimate.

It's not automatically "the model can't learn the patterns." 124M *can* learn github code patterns to ~3.0. So I'd reframe Problem 3 as "check your eval harness and dropout setting" before concluding capacity/data is the wall.

**Option C (train longer) is underrated *if* loss was still dropping.** At 427k iters with monotonic decrease, you weren't compute-saturated. But the diagnosis is right that data quality caps how low you can go — cleaner data shifts the asymptote down, more steps just walks you toward whatever asymptote your data allows.

### What I'd actually do, in order

1. **Swap tokenizer to StarCoder's** (`bigcode/starcoder` tokenizer via `tiktoken`/HF). Biggest cheap win for code; fixes the "spaces" symptom at the root.
2. **Swap data to `bigcode/the-stack-dedup`** (or filter github-code, but swapping is less work than writing a cleaner). Pick 3–5 languages, not all — fewer languages = denser signal at 124M.
3. **Fix the eval** — verify dropout is off during val loss measurement and that your val split is a representative random shuffle, not a contiguous chunk. Re-confirm the train>val gap.
4. Only then consider longer training or NL mixing.

The diagnosis's instinct (data > everything at this scale) is correct and Karpathy-aligned. I'd just kill the space-token panic and tokenizer-blind framing, and verify the train/val inversion before trusting the "underfitting" conclusion.

A quick sanity filter if you do stay on github-code rather than swapping:

```python
def keep(text: str) -> bool:
    n = len(text)
    if n < 200:                      # config stubs
        return False
    if text.count('<') / n > 0.05:   # HTML/javadoc heavy
        return False
    head = text[:600].lower()
    if ('copyright' in head or 'license' in head) and 'def ' not in head and '{' not in head[:200]:
        return False                 # license-header-dominated
    return True
```

But honestly — swapping to a deduplicated curated set + a code tokenizer will beat any amount of regex cleaning on the raw dump.

**References:**

- [DeepSeek-Coder-V2 paper (data mixture)](https://arxiv.org/abs/2406.11931)
- [DeepSeek-Coder paper (87/10/3 mix, repo-level dedup)](https://arxiv.org/abs/2401.14196)
- [StarCoder2 and The Stack v2](https://arxiv.org/abs/2402.19173)
- [The Stack (dedup, license filtering)](https://arxiv.org/abs/2211.15533)
- [bigcode/the-stack-dedup on HF](https://huggingface.co/datasets/bigcode/the-stack-dedup)
