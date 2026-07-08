---
audio: false
generated: true
image: false
lang: en
layout: post
title: ClimbMix-400B Construction and Use
translated: false
type: note
---

Question: What is the ClimbMix-400B dataset, and how is it constructed?

Answer:

ClimbMix (also called Nemotron-ClimbMix, and packaged by Karpathy as `karpathy/climbmix-400b-shuffle` for nanochat/nanoGPT-style training) is a 400-billion-token pretraining corpus produced by NVIDIA as the output artifact of the **CLIMB** framework (CLustering-based Iterative Mixture Bootstrapping), published at NeurIPS 2025.

**Pipeline that produces it:**

1. **Source merge**: Combine Nemotron-CC (NVIDIA's filtered Common Crawl derivative) with the smollm-corpus.
2. **Semantic clustering**: Embed all documents, then cluster the combined corpus into 20 semantic clusters. This filtered/reorganized corpus (1.2T tokens) is released separately as **ClimbLab** — a research playground for mixture experiments.
3. **CLIMB-search**: Iteratively search for the optimal *mixture weight* across those 20 clusters using a small proxy model (350M) + a predictor model that estimates downstream performance from a candidate mixture, rather than training every candidate mixture to convergence. This is the "iterative bootstrapping" — proxy-model results predict which mixtures the target-size model will do well on.
4. **Extraction**: Using the discovered optimal mixture ratios, sample **400B tokens** from ClimbLab clusters → this is **ClimbMix**.

**Why it matters / what the paper claims:**
CLIMB embeds and clusters large-scale datasets in a semantic space, then iteratively searches for optimal mixtures using a smaller proxy model and a predictor, enabling domain adaptation without relying solely on curated data. A 950M-parameter model continuously trained on 400B ClimbMix tokens exceeds Llama-3.2-1B by 2.0% averaged across 12 general reasoning tasks, and optimizing the mixture for a specific domain like Social Sciences yields a 5% improvement over random sampling. On the underlying search method (before the final ClimbMix extraction), the 350M target model with CLIMB-discovered mixtures achieves 54.83% average accuracy vs 52.17% for random mixing and 53.78% for the RegMix baseline.

**Practical uplift over this — how you'd actually pull it for a training run:**

```python
# Karpathy's shuffled HF release — this is what nanochat/nanoGPT-style pretrain scripts pull
from datasets import load_dataset

ds = load_dataset("karpathy/climbmix-400b-shuffle", streaming=True, split="train")

for i, row in enumerate(ds):
    text = row["text"]
    # tokenize, pack into your BPE-tokenized .bin shards
    if i > 10:
        break
```

This downloads the ClimbMix dataset from Hugging Face, trains a BPE tokenizer, and writes sharded binary data files — about 2 minutes on a fast VM with good network, cached locally so you only run it once per instance. This is exactly the corpus used in Karpathy's overnight-autoresearch nanoGPT loop — `val_bpb` on ClimbMix is the benchmark metric that gets optimized turn over turn.

**How it differs from FineWeb-Edu / DCLM (what you'd compare against for your own GPT-2-760M-on-MI300X runs):** those use heuristic quality filters (classifier scores, dedup rules) applied *before* mixing, with mixture ratios usually hand-tuned or uniform. ClimbMix instead treats the mixture ratio itself as a search variable optimized against actual downstream proxy-model performance — closer to a "hyperparameter search over data composition" than a filtering pipeline. If you're already deep into nanochat's data prep, the interesting delta to inspect is: does replacing your current data mix with a CLIMB-style proxy-search over your own domain clusters (code / math / general web) beat a hand-tuned ratio at your 760M scale? That's a cheap ablation to run on the MI300X given you already have the proxy-training infra from nanochat.

References:

- [CLIMB: CLustering-based Iterative Data Mixture Bootstrapping (NVIDIA Research)](https://research.nvidia.com/labs/lpr/climb/)
- [arXiv:2504.13161 — Nemotron-CLIMB paper](https://arxiv.org/abs/2504.13161)
- [karpathy/climbmix-400b-shuffle on Hugging Face](https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle)
- [Run Karpathy's autoresearch loop on GPU VM — Spheron Blog](https://www.spheron.network/blog/karpathy-autoresearch-spheron-gpu/)
