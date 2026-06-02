---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Testing Generalization with Unseen Elements
translated: false
type: note
---

In Ilya Sutskever's NeurIPS 2024 Test of Time Award talk on his 2014 "Sequence to Sequence Learning with Neural Networks" paper (and related early work like his PhD thesis on RNN language modeling), he reflected on early efforts to build generalizing neural language models. A key challenge was ensuring models didn't just memorize training data but could handle novel inputs—i.e., avoiding overfitting.

The specific "naive way" he referenced for detecting this involves testing the model on **unseen words or n-grams (multi-word sequences) not present in the training corpus (often called the "database")**.

### Why This Approach?
- **Overfitting risk in early language models**: Simple baselines like n-gram models (e.g., bigrams or trigrams) often "overfit" by only predicting fluently if the exact sequence appeared multiple times in training. They assign near-zero probability to anything novel, failing to generalize.
- **Naive detection test**: To check for true generalization (not overfitting), train on a held-out validation/test set engineered with deliberate "unseen" elements:
  - Replace common phrases with invented but plausible ones (e.g., in his thesis, testing sentence completion on a fake citation like "(ABC et al., 2003)"—a string the model had never encountered due to its unnatural capitalization and author name).
  - Measure if the model assigns reasonable probabilities, generates coherent completions, or maintains low perplexity/BLEU scores despite the novelty.
- If the model fails (e.g., high perplexity or incoherent output) on these unseen items but excels on seen training data, it's overfitting (memorizing specifics rather than learning patterns). If it succeeds, it's generalizing via learned representations (e.g., LSTM states capturing syntax/semantics).

### Examples from His Work
- **In the seq2seq paper (2014)**: They used a fixed vocabulary (80k French words, 160k English), replacing out-of-vocabulary (OOV) words with "UNK." To detect generalization issues, they penalized BLEU scores for OOV occurrences and plotted performance vs. "average word frequency rank" (rarer = more unseen-like). The LSTM handled rare/unseen words well without degradation, unlike baselines.
- **In his PhD thesis (2013, on RNN language modeling)**: For structured sentence completion, they tested on entirely novel strings like "(ABC et al., 2003)" (unseen in training due to rarity). The multiplicative RNN (MRNN) generalized robustly (e.g., predicting year/context correctly), while n-gram baselines couldn't unless exact matches existed—highlighting their overfitting.

This "check unseen words/n-grams" test was a straightforward, early heuristic before advanced techniques like dropout or validation curves. Sutskever noted in the talk how such insights drove scaling to modern LLMs, where generalization on vast unseen data remains core.

[Sequence to Sequence Learning with Neural Networks (arXiv PDF)](https://arxiv.org/pdf/1409.3215.pdf)
[Ilya Sutskever PhD Thesis (PDF)](https://www.cs.utoronto.ca/~ilya/pubs/ilya_sutskever_phd_thesis.pdf)
[Ilya Sutskever NeurIPS 2024 Talk Video](https://www.youtube.com/watch?v=YD-9NG1Ke5Y)
