---
audio: false
generated: true
image: false
lang: en
layout: post
title: Normal Behavior for Small AI Models
translated: false
type: note
---

Yes, this is normal for a 124M parameter model. Here's why:

1. **Small model**: 124M params is tiny by today's standards. GPT-2 124M can produce grammatically correct SEC-style text but has very limited ability to maintain contextual coherence over long generations.

2. **Topic drift**: The prompt talks about net losses and healthcare, but the model drifts to "e-commerce" and "operating divisions" — it's generating statistically plausible SEC filing language without really "understanding" the prompt content.

3. **Repetition**: "e-commerce and e-commerce" repeated many times is a classic degeneration pattern for small language models. They lack the capacity to track what they've already said.

4. **Training data**: The model was trained on all SEC EDGAR filings (not just healthcare), so it has a broad but shallow understanding of filing language.

What you're seeing is the realistic ceiling of a 124M model. To get better output you'd need:
- **Larger model**: 350M+ params would maintain topic coherence much better
- **More training data/longer training**: The model was trained for 47k steps
- **Fine-tuning on a specific domain**: e.g., only healthcare SEC filings

The model is working correctly — it's just at its capacity limit. For a demo/proof-of-concept it's fine; for production you'd want at least a 1-3B parameter model.
