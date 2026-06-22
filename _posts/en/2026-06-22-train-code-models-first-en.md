---
audio: false
generated: true
image: false
lang: en
layout: post
title: Train Code Models First
translated: false
type: note
---

**Question:** Should I learn to train small code models first? Is code easier to train on due to its structural patterns? And is Anthropic's focus on coding a key reason it overtook OpenAI in market cap?

**Answer:**

## Why Code Models Train Faster (Loss Drops Faster)

Your intuition is exactly right — and the hermes quote nails it mechanically:

**Entropy is lower in code than natural language.**

```python
# Rough intuition: bits per token
# Natural language: ~3-4 bits/token (high entropy, unpredictable)
# Code: ~1-2 bits/token (lower entropy, constrained grammar)

# A model predicting the next token in:
"The quick brown fox..."    # genuinely hard — many continuations
"def __init__(self, "      # almost certain: identifier or `)`
```

Shannon entropy of code << natural language. Cross-entropy loss is measuring exactly this — how surprised the model is. Less surprise → loss drops faster.

**Mechanistically:**
- Token `{` after `if condition` → near-deterministic
- Indentation after `:` in Python → deterministic given context
- `import` at file top → high probability mass on a small set
- Function bodies repeat structure (docstring → args → logic → return)

The model allocates less capacity to "what word comes next?" and more to "what is the logic here?" — which is the actually hard and useful part.

## Should You Train Small Code Models First?

**Yes, for these concrete reasons:**

**1. Faster iteration cycles**
Loss curves are smoother and drop more predictably. You'll see meaningful perplexity improvement in hours on an RTX 4070, not days. This means faster hypothesis-test loops — exactly your learning style.

**2. Eval is objective**
Did the generated code run? Did the tests pass? Natural language quality is subjective. Code quality is measurable:
```bash
# Your eval loop can literally be:
python -m pytest generated_code_test.py
# Pass rate = your metric. No human eval needed.
```

**3. Dataset engineering is easier**
GitHub + The Stack + StarCoder data → already cleaned, deduplicated, filtered by language. Natural language datasets require way more curation judgment.

**4. The patterns compound your existing knowledge**
You already know what good Python looks like. You can read loss curves and immediately understand *why* the model is confused (syntax? API names? logic structure?). This is the "build by understanding" loop Karpathy advocates.

**5. Smaller effective vocab → smaller embedding tables → fits on RTX 4070**
Python has ~10k meaningful tokens in practice. You can train a competent small code model at 125M-360M params on your workstation without heroics.

## Anthropic vs OpenAI Market Cap — Is Code the Reason?

Partially, but let me be precise rather than just affirming you:Yes — your thesis is validated by actual data, not just intuition:

Anthropic's growth accelerated sharply in late 2025 following the release of Claude Opus 4.5, a model whose coding abilities rapidly turned Claude Code into one of the most popular developer tools in Silicon Valley, becoming something of a cultural phenomenon among software engineers.

Anthropic's revenue exploded thanks to Claude Code, reaching a $47 billion revenue run rate — up from $30 billion earlier this year and $10 billion last year — and its $965 billion Series H valuation now puts it above OpenAI.

Ramp data showed Anthropic overtook OpenAI among business users in April 2026, with Anthropic adoption at 34.4% of businesses vs. OpenAI's 32.3%.

So **yes, coding was the primary wedge**. The disciplined focus paid off.

---

## Your Learning Path

Given all this — here's the concrete sequence I'd recommend:

```
1. Train a small code model (125M) on Python subset of The Stack
   → nanoGPT architecture, measure loss drop rate vs. text baseline
   → eval with: does it produce syntactically valid Python? pass rate on simple problems?

2. Add instruction tuning (SFT on code instruct pairs)
   → humaneval / mbpp as your benchmark — objective, automated

3. Then move to text models with the intuitions you've built
   → You'll understand loss landscapes, tokenization tradeoffs much deeper

4. Then LoRA fine-tuning of existing code models (StarCoder2, DeepSeek-Coder)
   → Much faster iteration — you're doing delta training, not from scratch
```

The sequence is: **from-scratch small code model → SFT → existing model fine-tuning → MoE understanding**. Your RTX 4070 handles steps 1-3 fine. Step 4 might push you to the AMD box.

Your original insight is the core one: **lower entropy → faster loss descent → faster feedback loops → better learning**. Train on code first, build the intuitions, then everything else compounds.

References:
- [Anthropic tops OpenAI as most valuable AI startup](https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html)
- [How Anthropic eclipsed OpenAI's valuation](https://invezz.com/news/2026/05/30/the-new-ai-king-how-anthropic-eclipsed-openais-valuation-and-leapt-to-965b/)
