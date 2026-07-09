---
audio: false
generated: true
image: false
lang: en
layout: post
title: Datasets for LLM Pretraining
translated: false
type: note
---

**Question:** Besides FineWeb, what other text datasets can I use for LLM pretraining?

**Answer:**

Here's the practical landscape, organized by what role each dataset plays in a training mix.

## General web-text (FineWeb alternatives/peers)

- **DCLM-Baseline** (DataComp-LM, ~3.8T tokens) — Apple/UW's classifier-filtered Common Crawl. On many benchmarks it matches or beats FineWeb-Edu per token; the DCLM paper's fastText quality classifier is worth studying on its own.
- **RefinedWeb** — ~600B tokens of aggressively deduplicated Common Crawl, used to train the Falcon family.
- **Dolma** (AI2, ~3T tokens) — fully open pipeline + data, powers OLMo. Best choice if you want to *reproduce* every filtering decision.
- **RedPajama v1/v2** — an open replication of LLaMA-style pretraining data under Apache 2.0; v2 ships with quality signals as columns so you can do your own filtering.
- **C4** — Google's cleaned Common Crawl snapshot built for T5; older and noisier, but small and standard for ablations.
- **Nemotron-CC** (NVIDIA, ~6.3T tokens) — combines classifier ensembles + synthetic rephrasing of low-quality docs. Interesting because it shows rewriting data with an LLM beats discarding it.
- **TxT360** — globally deduplicated across 99 CC snapshots + 14 curated sources.
- **Raw Common Crawl** — the bedrock everything above derives from; a monthly crawl is hundreds of TiB across ~2B pages. Realistically you keep 2–10% of bytes after language ID, dedup, and quality filtering — only go here if you're building your own pipeline (which, given your interests, is a genuinely good learning project).

## Curated / multi-source

- **The Pile** — 825 GB across 22 diverse sources (books, papers, GitHub), ~300B tokens. Old but great for nanoGPT-scale runs because of its diversity per token.
- **SlimPajama** — deduplicated 627B-token version of RedPajama.
- **Wikipedia + Stack Exchange + Project Gutenberg** — small, high-quality, standard upsampled components in nearly every mix.

## Code

- **The Stack v2** — 67.5 TB of permissively licensed source code across 600+ languages, powering StarCoder2. Even for a "text" model, 5–15% code in the mix measurably improves reasoning.
- **StarCoderData** — the filtered training subset if you don't want raw Stack.

## Math (highest-leverage per token for reasoning)

- **OpenWebMath** — ~15B tokens of LaTeX-preserving math from the web
- **FineMath** — 54B tokens, educational math filtered similarly to FineWeb-Edu
- **Nemotron-CC-Math** — a 133B-token high-quality math pretraining set
- **Proof-Pile-2** — math + formal proofs + arXiv, used for Llemma

## Multilingual

- **FineWeb-2** — the multilingual FineWeb covering 1000+ languages (includes strong Chinese subsets)
- **HPLT 2.0** — 4.5T tokens across 75 languages
- **MADLAD-400** — 3T tokens, 400 languages, from Google

## Practical recipe for your scale

For a GPT-2 760M / nanoGPT-class run (~10–100B tokens, MI300X), a strong mix:

```python
# Chinchilla-ish mix for a ~1B model, streaming from HF
from datasets import load_dataset, interleave_datasets

mix = interleave_datasets([
    load_dataset("HuggingFaceFW/fineweb-edu", "sample-100BT", split="train", streaming=True),
    load_dataset("mlfoundations/dclm-baseline-1.0", split="train", streaming=True),
    load_dataset("bigcode/starcoderdata", data_dir="python", split="train", streaming=True),
    load_dataset("HuggingFaceTB/finemath", "finemath-4plus", split="train", streaming=True),
], probabilities=[0.55, 0.25, 0.10, 0.10], seed=42)
```

Two higher-leverage moves than swapping datasets:

1. **Ablate DCLM vs FineWeb-Edu yourself** at 760M / 10B tokens — results differ by benchmark, and running the ablation teaches you more than any leaderboard. Karpathy's nanochat uses FineWeb-Edu shards precisely because it's the reliable default, not because it always wins.
2. **Study the filtering classifiers**, not just the outputs. FineWeb-Edu's is a lightweight regressor trained on Llama-3-70B educational-value annotations over embeddings — you can retrain that pipeline for a custom domain (e.g., an agent/tooling-focused corpus) in a weekend on your 4070.

**References:**

- [FineWeb-Edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- [The Top 10 LLM Training Datasets for 2026 — iMerit](https://imerit.ai/resources/blog/the-top-10-llm-training-datasets-for-2026/)
- [Best LLM Training Datasets for 2026 — SpyderProxy](https://spyderproxy.com/blog/best-llm-training-datasets)
- [Top 10 LLM Training Datasets — ODSC](https://opendatascience.com/the-top-10-llm-training-datasets-for-2026/)