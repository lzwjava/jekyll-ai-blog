---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC Filing Output Quality Fix
translated: false
type: note
---

Output is now coherent SEC filing text with real financial numbers and proper structure. Here's what was wrong and what I fixed:

== ROOT CAUSE ==

  Two problems in server.py that degraded output quality vs nanoGPT native:

  1. SEC_SYSTEM prefix — "The following are excerpts from SEC EDGAR filings..."
     was prepended to every prompt. The model was NOT trained with this prefix,
     so it confused the context and produced repetitive/incoherent output.

  2. top_p=0.9 sampling — nanoGPT uses top_k=200 (retains top 200 tokens,
     clamps rest to -inf). top_p=0.9 (nucleus sampling) with a 124M model
     produces worse results — too much probability mass leaks to unlikely tokens.

== FIX ==

  server.py updated:

- Removed SEC_SYSTEM prefix — prompts go directly to the model as-is
- Switched from top_p=0.9 to top_k=200 (matches nanoGPT sample.py)
- Default temperature: 0.7 → 0.8 (matches nanoGPT)

== COMPARISON ==

  Before (top_p + SEC prefix):
    "Our principal business is our principal executive office in San Francisco,
     California and is located in The San Francisco, California..."

  After (top_k=200, no prefix):
    "$7,878,832 ... $8,798,871 ... The following table summarizes the change
     in the Company's pre-tax income (loss) attributable to non-controlling
     interests... ASC 815, Hedging Activities"

== REMAINING NOTE ==

  The nanoGPT native model (ckpt.pt + model.py) still produces slightly better
  output than the HF transformers version — likely due to the weight conversion
  (vocab 50304→50257 trimming, zero biases added). But the gap is much smaller
  now. If you want to go further, we can upload ckpt.pt + model.py to RunPod
  and use the native model class instead of transformers.
