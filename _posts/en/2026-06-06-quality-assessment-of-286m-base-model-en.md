---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quality Assessment of 286M Base Model
translated: false
type: note
---

Here's the quality assessment of the 286M base model at step 87k:

```
QUALITY ASSESSMENT — nanochat d12 (286M params, step 87k, val_bpb=0.866)

GOOD:
  ✓ "Capital of France is Paris" — gets the fact right
  ✓ "Once upon a time" — coherent story structure, character names, narrative
  ✓ "Meaning of life" — coherent philosophical prose, sensible sentences
  ✓ "In 2025, AI" — reasonable tech prose, good grammar
  ✓ "Theory of relativity" — factually correct (speed of light, equivalence principle)
  ✓ General fluency is solid — sentences flow, grammar is mostly correct

WEAK:
  ✗ "def fibonacci(n):" — no actual code, hallucinates a dictionary definition
  ✗ "import torch" — treats it as a dictionary/wiki word, not Python code
  ✗ Repetition (Corsica listed twice, "She was very poor" repeated)
  ✗ Factual drift (Sardinia as a department of Paris, made-up numbers)

VERDICT:
  For a 286M base model, this is solid. It has basic world knowledge,
  coherent prose, and reasonable grammar. The main gaps are:
  - No code understanding (expected at this scale without SFT)
  - Repetition loops (common in small models)
  - Fact hallucination after initial correct answers

  For reference: GPT-2 124M (2019) was much worse at this bpb range.
  This model is in the "useful but needs SFT for chat/code" zone.
  The extended training to 130k should push bpb below 0.85 and
  improve coherence further.
```

The model is in good shape — base models at 286M are expected to be weak at code and hallucinate facts. The real unlock comes from SFT (chat fine-tuning) and RL alignment, which nanochat supports via `scripts/chat_sft.py` and `scripts/chat_rl.py`.
