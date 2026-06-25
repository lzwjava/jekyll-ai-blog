---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dirty Data, Garbage Code
translated: false
type: note
---

Here's the complete diagnosis:

---

TRAINING DIAGNOSIS
==================

The model trained correctly (427k iters, final val_loss 3.466) and DID learn
something real — perplexity went from 50,304 (random) to 32.3. But the
generation output is garbage. Here's why:

PROBLEM 1: TRAINING DATA IS TOO DIRTY (main culprit)
  The codeparrot/github-code dataset is a raw GitHub dump, not curated:
    - Only ~54% actual code
    - ~31% license/copyright boilerplate headers
    - ~12% HTML docs (javadoc, doxygen, generated pages)
    - ~2% config/JSON files

  A 124M model can't learn meaningful code patterns when nearly half
  the training data is noise.

PROBLEM 2: SPACE TOKEN DOMINATION
  26% of ALL tokens in the dataset are single space (token 220).
  The model learned the safest prediction is always a space:
    After "def quicksort(arr):" → 46.8% space, 10.8% newline
  This is code indentation being interpreted as signal, not structure.

PROBLEM 3: UNDERFITTING, NOT OVERFITTING
  Train loss (~3.63) is HIGHER than val loss (~3.54).
  The model hasn't memorized — it simply can't learn the patterns.
  It needs either cleaner data or more capacity.

PROBLEM 4: VAL LOSS OF 3.466 (perplexity 32) IS TOO HIGH FOR CODE
  For reference:
    GPT-2 124M on OpenWebText (English): ~2.85 loss (perplexity ~17)
    CodeParrot-small 110M on code:       ~3.0  loss (perplexity ~20)
    This model:                           3.47 loss (perplexity ~32)

  At perplexity 32, the model can't reliably predict the next token,
  so generation degrades into the most common token (spaces).

WHAT TO DO
==========

Option A (best): Clean the data and retrain

- Filter out HTML-heavy files (count '<' > threshold)
- Remove files that are mostly license/copyright headers
- Remove files < 200 chars (config stubs)
- Deduplicate boilerplate
- This alone could drop loss to ~3.0-3.1

Option B: Use a curated dataset

- The Stack v2 (BigCode) — already filtered for quality
- StarCoder training data
- Or just filter codeparrot/github-code before tokenizing

Option C: Train much longer

- Loss was still decreasing at 427k iters
- Maybe 800k-1M iters would help, but data quality is the bottleneck

Option D: Convert to GGUF and use as a code-completion assist

- Even at perplexity 32, it has SOME code knowledge
- Could work for autocomplete-style tasks with constrained decoding
- But don't expect it to generate full functions

Want me to write a data-cleaning script to filter the parquet files and
re-tokenize? That's the highest-impact fix.
