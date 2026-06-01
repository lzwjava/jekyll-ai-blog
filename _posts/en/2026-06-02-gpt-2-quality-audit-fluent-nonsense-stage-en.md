---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPT-2 Quality Audit: Fluent Nonsense Stage"
translated: false
type: note
---

Here's the quality audit:

```
======================================================================
  QUALITY AUDIT — GPT-2 760M (step 76K/445K, val_loss=3.16)
======================================================================

  PROMPT 1: "The history of artificial intelligence"
  ───────────────────────────────────────────────────
  ✓ Grammatically correct sentences
  ✓ Coherent paragraph structure
  ✓ Relevant topic (AI, computer science)
  ✗ Factually wrong (made-up conferences, dates)
  ✗ Repetitive ("structure of the universe" x3)
  ✗ Loses coherence after ~100 tokens
  ✗ Mixes in unrelated content (Yale-New Haven Teachers Institute)
  VERDICT: Wikipedia-flavored text salad. Looks right, reads wrong.

  PROMPT 2: "def fibonacci(n):"
  ───────────────────────────────────────────────────
  ✗ Completely fails at code
  ✗ Generates ISBN numbers, bibliography entries
  ✗ One sample is pure gibberish ("B2p22:B3:B2p2p3...")
  VERDICT: No code capability at all.

  PROMPT 3: "The capital of France is"
  ───────────────────────────────────────────────────
  ✗ Factually wrong ("Liguestas, in the province of Aragon")
  ✗ One sample says "Paris" then immediately contradicts itself
  ✗ Generates fake geography (Korea-Yunsu border, Sichuan as capital of China)
  ✓ Grammatically coherent
  VERDICT: Fluent but hallucinates confidently.

  PROMPT 4: "Once upon a time, there was a robot who"
  ───────────────────────────────────────────────────
  ✓ Reasonable story structure
  ✓ Some creative elements
  ✗ Loses plot quickly, becomes incoherent
  ✗ Injects Bible references randomly
  ✗ One sample veers into video game essay
  VERDICT: Has story-like structure but no real narrative logic.

======================================================================
  OVERALL ASSESSMENT
======================================================================

  What it CAN do:
    - Generate grammatically correct English
    - Maintain topic for ~50-100 tokens
    - Produce plausible-looking text structure (lists, paragraphs)
    - Mimic writing styles (Wikipedia, academic, narrative)

  What it CANNOT do:
    - Factual accuracy (hallucinates confidently)
    - Code generation (completely broken)
    - Long-range coherence (loses thread after ~100 tokens)
    - Reasoning or logic
    - Self-consistency (contradicts itself)

  Comparison:
    - Better than random (obviously)
    - Worse than GPT-2 1.5B (2019) which had similar loss
    - Comparable to a very early autocomplete
    - NOT usable for any production task

  Bottom line:
    At val_loss=3.16, the model has learned language statistics
    but not language understanding. It's a "stochastic parrot"
    in the most literal sense — it produces plausible-looking
    text without any comprehension of meaning.

    To get usable quality, you'd need:
    - val_loss < 2.5 (roughly GPT-2 level)
    - Which means more training or a larger model
    - Or: use the checkpoint as a base for fine-tuning

======================================================================
```

The model is at the "fluent nonsense" stage. It generates text that *looks* like English but has no factual grounding or logical coherence. This is expected at 17% training completion with val_loss=3.16 — it's learned the statistical structure of language but not the semantics.