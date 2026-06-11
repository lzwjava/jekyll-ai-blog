---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Christopher Ré: Stanford AI Professor"
translated: false
type: note
---

**Question:** Who is Christopher Ré at Stanford?

**Answer:**

Christopher (Chris) Ré is a professor in the Department of Computer Science at Stanford University, in the Stanford AI Lab (SAIL), affiliated with the Machine Learning Group and the Center for Research on Foundation Models (CRFM). He runs the **Hazy Research** lab — and if you've been studying transformer internals and efficient attention, you've almost certainly been using his lab's work without realizing it.

Why he matters for your trajectory specifically:

**FlashAttention came out of his lab.** Tri Dao was his PhD student, and FlashAttention (the IO-aware exact attention kernel that tiles Q/K/V through SRAM to avoid materializing the N×N attention matrix in HBM) is now the default in basically every serious training stack — including nanoGPT when you use `F.scaled_dot_product_attention`. The same lineage produced FlashFFTConv and the broader "hardware-aware algorithm design" school of thought.

**The state space model line (S4 → Mamba) also traces to him.** Albert Gu (Mamba co-author, with Tri Dao) did his PhD under Ré. His lab's recent work includes Zoology (measuring recall in efficient language models), Monarch Mixer (a sub-quadratic GEMM-based architecture), and Hyena/HyenaDNA for long-range sequence modeling — essentially the research program asking "what replaces or augments attention?"

**Data-centric AI.** Before the foundation model era, he was known for weak supervision — Snorkel (programmatic labeling instead of hand-labeling) came from his lab. He co-founded SambaNova and Snorkel AI, plus two companies acquired by Apple: Lattice (DeepDive) in 2017 and Inductiv (HoloClean) in 2020. He's also a co-founder of **Together AI** (the inference/training cloud you may have hit through OpenRouter). His lab's research has fed into scientific efforts like Evo, a DNA foundation model, and products at Apple, Google, YouTube, and more.

Background and credentials: he was awarded a MacArthur Fellowship in 2015, and his work won best paper at top venues across three fields — PODS 2012 (database theory), SIGMOD 2014 (database systems), and ICML 2016 (machine learning) — plus the NeurIPS 2020 and PODS 2022 test-of-time awards. That database-systems-first background is the key to understanding his style: he treats ML as a systems problem where data movement and data quality dominate, which is exactly the FlashAttention insight (attention is memory-bound, not compute-bound).

If you want to go deeper, the highest-leverage reading order for you given your nanoGPT/MI300X work: (1) the FlashAttention paper + Triton implementation, (2) his lab blog posts on "Zoology" and associative recall — they explain *why* attention beats SSMs on certain subtasks, which is directly relevant to your DeepSeek MoE exploration, (3) the Mamba paper. His lab publishes readable code for nearly everything at github.com/HazyResearch.

**References:**

- [Chris Ré's homepage — Stanford CS](https://cs.stanford.edu/~chrismre/)
- [Stanford CS faculty profile](https://www.cs.stanford.edu/people/chris-re)
- [Wikipedia — Christopher Ré](https://en.wikipedia.org/wiki/Christopher_R%C3%A9)
- [Google Scholar profile (~77k citations)](https://scholar.google.com/citations?user=DnnCWN0AAAAJ)
