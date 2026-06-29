---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR-GPT Paper Update
translated: false
type: note
---

Those are just the standard "undefined citation" warnings from a first pdflatex pass — pre-existing, not from my changes. No errors.

Done. Two changes to `/Users/lzwjava/projects/sec-edgar-gpt/sec-edgar-gpt.tex`:

1. Title updated: "SEC-EDGAR-GPT: A GPT-2 (124M) Language Model Trained from Scratch on SEC EDGAR Filings"

2. New Section 8 "Model Serving" added (between Discussion and Conclusion) with four subsections:
   - The bias=False Conversion Problem — the core correctness argument about why HF conversion is risky (fused c_attn weight layout, transposition errors)
   - Sampling Parity — nanoGPT's 10-line generate() vs HF's 2000-line dispatcher
   - Dependency Overhead — torch+tiktoken only, no transformers/safetensors/tokenizers
   - When Hugging Face or vLLM Would Be Preferred — honest about the tradeoffs (batched serving, ecosystem, from_pretrained interface)

PDF compiles clean at 21 pages.
