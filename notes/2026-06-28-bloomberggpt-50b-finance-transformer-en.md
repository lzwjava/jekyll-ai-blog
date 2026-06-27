---
audio: false
generated: true
image: false
lang: en
layout: post
title: "BloombergGPT: 50B Finance Transformer"
translated: false
type: note
---

**Question:** Explain and introduce BloombergGPT (Wu et al., 2023, arXiv:2303.17564) — a large language model for finance.

**Answer:**

BloombergGPT is a 50B-parameter decoder-only transformer trained by Bloomberg in 2023, notable as one of the first serious attempts at a *domain-specialized* foundation model built from scratch rather than fine-tuned. The core thesis: a model trained on a mix of finance-heavy and general data outperforms equally-sized general models on financial NLP without sacrificing general-purpose capability.

**The data — the actual contribution.** The headline isn't the architecture (it's vanilla BLOOM-style), it's **FinPile**: a 363B-token financial corpus assembled from Bloomberg's proprietary archives — news, filings, press releases, Bloomberg-authored content, web data, and Bloomberg terminal messages going back decades. They mixed this ~50/50 with a public general corpus (The Pile, C4, Wikipedia) for a **~700B token** training set, of which ~569B tokens were actually consumed (1 epoch-ish, they ran out of compute budget before a full second pass). The lesson: at the time, proprietary high-quality domain data was the moat, not model tricks.

**Architecture specifics:**
- 50B params, 70 layers, 40 attention heads, hidden dim 7680
- Decoder-only causal LM, ALiBi positional encoding (not RoPE), trained with Unigram tokenizer (sized to 131,072 — large vocab to handle financial tokens/numbers efficiently)
- Trained on 64×8 = 512 A100 40GB GPUs, ~53 days
- Chinchilla-aware sizing: they explicitly picked 50B params for ~700B tokens to sit near the compute-optimal frontier given their ~1.3M GPU-hour budget.

**Why 50B and not bigger?** Pure Chinchilla math. Given a fixed FLOP budget `C ≈ 6·N·D` (N=params, D=tokens), they solved for the N/D split that minimizes loss. With ~700B tokens available, 50B params lands near optimal. This is the same `N ≈ D/20` Chinchilla ratio reasoning — worth internalizing because it's the lens for every "how big should my model be" decision, including your own training runs.

**Results.** It beat similarly-sized open models (GPT-NeoX 20B, OPT 66B, BLOOM 176B) on internal financial benchmarks — sentiment classification, NER, financial QA (FiQA, ConvFinQA, FPB) — while staying competitive on general benchmarks (BIG-bench, MMLU-style tasks). Notably it did *not* beat much larger general models on general tasks, but the point was it didn't collapse on them either.

**Why it matters now / what aged poorly.** Two things to take from it:

1. **The "train from scratch on domain data" thesis is largely dead.** By late 2023, fine-tuning / continued-pretraining strong open models (Llama, Mistral, Qwen, DeepSeek) became far cheaper and competitive. Nobody would spend 1.3M GPU-hours from scratch for a 50B finance model today — you'd LoRA or do continued pretraining on a strong base. BloombergGPT was the high-water mark of the "from-scratch vertical model" era right before it became obsolete.
2. **The data moat thesis survived.** FinPile is still the interesting part. The reproducible insight for you: proprietary, well-curated domain corpora + a strong open base + cheap fine-tuning is the winning recipe now. You worked at banks — you know financial text (filings, Bloomberg-style news) is messy and specialized; the value was always in the corpus engineering, not the transformer.

For your trajectory: the relevant follow-on reading is FinGPT (the open, fine-tuning-based rebuttal that did in adapters what Bloomberg did with $1M+ of compute) — it directly demonstrates why the from-scratch approach lost.

**References:**

- [BloombergGPT: A Large Language Model for Finance (arXiv:2303.17564)](https://arxiv.org/abs/2303.17564)
- [FinGPT: Open-Source Financial LLMs (arXiv:2306.06031)](https://arxiv.org/abs/2306.06031)
- [Training Compute-Optimal LLMs / Chinchilla (arXiv:2203.15556)](https://arxiv.org/abs/2203.15556)
