---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Three Endoftext Tokens as Standard
translated: false
type: note
---

You **can** technically use just one `<|endoftext|>` (token 50256) as a document separator — it would still give you clear boundaries between documents, and the model would learn not to continue across them most of the time.

But in practice, almost everyone who trains GPT-2-style models on web text (OpenWebText, FineWeb, RedPajama, C4-derived datasets, etc.) uses **exactly three** for very good reasons that became the de-facto standard very early on:

### 1. It matches (or very closely mimics) what OpenAI did with the original GPT-2 WebText

- OpenAI never released WebText, but the original OpenWebText replication (Skylion007, 2019) and basically every clone since then inserts **three** `<|endoftext|>` tokens between documents.
- When Andrej Karpathy reproduced GPT-2 results in nanoGPT on OpenWebText, he followed the same convention.
- When he later switched to FineWeb-10B/100B samples in his lectures, he kept the exact same format: three separators.
- EleutherAI (GPT-NeoX/J), Stability, Mistral, etc., all do the same when processing CommonCrawl-style data.

Because of this, using three makes your data preparation identical to the datasets that produced the published GPT-2 perplexity numbers and downstream performance everyone compares against.

### 2. It makes accidental merging almost impossible during packing

Modern trainers (nanoGPT, llm.c, HuggingFace, Megatron, etc.) pack multiple documents into the same training sequence to reach the full context length (1024 for GPT-2, 2048/4096/128k now).

If you only use one `<|endoftext|>`, there is a tiny chance that a bug, an off-by-one error, or a weird edge case causes two documents to be concatenated without any separator. That creates a horrible training signal (the model suddenly learns to continue one random webpage into another).

With **three** in a row, even if something goes wrong and one token gets dropped or misread, you still have two left → the boundary is preserved. It’s a cheap form of error-detecting redundancy.

### 3. It makes the separator uniquely identifiable and unconfusable

- A single 50256 can theoretically appear in the middle of real content (extremely rarely, but possible — the tokenizer is not perfect, and some pages contain the literal string `<|endoftext|>` or byte sequences that encode to it).
- Three identical rare tokens in a row will **never** appear naturally in real web text. So any post-processing, debugging, or dataset inspection can instantly spot document boundaries with zero false positives.

### 4. It has zero downside

- Three tokens cost essentially nothing (≈0.00001% of a 300B–1T token dataset).
- The model learns very quickly that `50256 50256 50256` means “definitely start fresh prediction here”.

### Summary

One would work fine for your own experiments, but three is the established convention because:

- it matches the original WebText / OpenWebText that GPT-2 was trained on,
- it adds robustness against bugs,
- it makes boundaries 100% unambiguous.

That’s why every public script you’ll find (Karpathy’s fineweb.py, the OpenWebText repo, HazyResearch flash-attention training code, etc.) uses exactly three — and why I recommended it to you.

If you ever want to compare your model’s perplexity or samples directly to GPT-2 / nanoGPT / FineWeb baselines, use three and you’re golden.
