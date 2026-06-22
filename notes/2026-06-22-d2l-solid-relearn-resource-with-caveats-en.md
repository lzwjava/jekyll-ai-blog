---
audio: false
generated: true
image: false
lang: en
layout: post
title: "d2l: Solid Relearn Resource with Caveats"
translated: false
type: note
---

**Question:** Is *Dive into Deep Learning* (d2l.ai) a good resource to relearn deep learning fundamentals, especially given my background in model training and LLM systems?

**Answer:**

d2l is genuinely one of the best DL textbooks that exists — interactive, code-first, covers everything from scratch to attention. For your background it's a solid relearn pass, but go in with the right expectations:

**What d2l does well:**
- Every concept has runnable code alongside math — matches your build-first style
- Covers the full stack: linear algebra → CNNs → RNNs → attention → transformers → modern training tricks
- Multiple framework implementations (PyTorch, JAX, MXNet)
- The attention chapter is actually rigorous — not hand-wavy

**Where it pulls punches (the Yin Wang critique you're gesturing at):**
- Never tells you which papers are genuinely important vs. incremental citation games
- Softens critiques — won't say "this architecture is a dead end" or "this loss function was a mistake"
- The "recommended practices" sections are often consensus opinion, not first-principles reasoning
- Skips the messy reality of training instability, loss spikes, gradient pathologies at scale
- No serious coverage of MoE, sparse attention, KV cache optimization — the stuff that actually runs at scale today

**For you specifically, I'd read it with this filter:**

The chapters worth deep attention given your trajectory:
- Ch 10-11: Attention mechanisms — read the math carefully, cross-reference with Karpathy's nanoGPT
- Ch 15: NLP/pretraining — bridges to what you're doing with GPT-2 training
- Ch 12: Computational performance — GPU utilization, parallelism

Skip or skim:
- Early CNN chapters — you know this
- RNN chapters — mostly historical, transformers ate this

**The Yin Wang version of this book doesn't exist yet** — that's actually the gap in your public knowledge base opportunity. Your blog + 9600 notes, written with that "which paper is actually load-bearing" energy, would be more valuable than d2l for serious practitioners. d2l is diplomatically written for academia. You could write the practitioner-honest version.

Relearning it is worth it — but treat it as a map, not the territory. The territory is the actual training runs you're doing on MI300X.
