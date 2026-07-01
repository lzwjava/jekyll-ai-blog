---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Download and GPT-3 Training Guide
translated: false
type: note
---

**Question:** Regarding the script `plan_and_download_fineweb_gpt3.py` — is downloading ~100B tokens from FineWeb good or bad, and is that expected? Also, how do you use the downloaded FineWeb data to train a GPT-3 style model?

---

**Answer:**

## Part 1: Is 100B Tokens Good, Bad, or Expected?

**It's a reasonable and intentional subset — not the full dataset.**

FineWeb is built from 96 snapshots of Common Crawl, spanning from 2013 to early 2024, and comprises **15 trillion GPT-2 tokens** of predominantly English text. So 100B tokens is only about **0.67%** of the full FineWeb dataset.

That said, 100B tokens is a perfectly legitimate target for a GPT-3 scale experiment:

- FineWeb is sufficiently large to train a Chinchilla-optimal model with more than **500 billion parameters**. So 100B tokens is enough to train a smaller GPT-3 style model (e.g. 1.3B–6.7B parameters) by Chinchilla scaling rules (roughly ~20 tokens per parameter).
- FineWeb-Edu is available in two sizes: 1.3T tokens and 5.4T tokens. If you're using the educational subset, 100B tokens is a meaningful chunk of the smaller version.
- The original GPT-3 paper (175B parameters) trained on ~300B tokens. So 100B tokens for a smaller reproduction is very reasonable.

**In short:** 100B tokens is a deliberate, practical subset — good for a research experiment or smaller GPT-3 reproduction. It's expected behavior for a planning/downloading script that targets a manageable slice of the dataset.

---

## Part 2: How to Train a GPT-3 Style Model on FineWeb Data

Here is the full pipeline:

### Step 1 — Download & Tokenize

Your script likely downloads FineWeb shards from Hugging Face. After downloading, tokenize with GPT-2's BPE tokenizer (tiktoken):

```python
import tiktoken
enc = tiktoken.get_encoding("gpt2")
tokens = enc.encode(text)
```

Save shards as binary `.bin` files (uint16 numpy arrays) — this is the standard nanoGPT format.

### Step 2 — Set Up Training Framework

Andrej Karpathy's `build-nanogpt` repo starts from an empty file and works toward a reproduction of GPT-2 (124M). If you have more patience or money, the code can also reproduce the GPT-3 models.

Clone it:

```bash
git clone https://github.com/karpathy/build-nanogpt
cd build-nanogpt
pip install torch numpy tiktoken
```

### Step 3 — Configure GPT-3 Hyperparameters

GPT-3 uses these key hyperparameters (vary by model size):

| Model | Layers | Heads | d_model | Params |
| --- | --- | --- | --- | --- |
| GPT-3 Small | 12 | 12 | 768 | 125M |
| GPT-3 Medium | 24 | 16 | 1024 | 350M |
| GPT-3 XL | 24 | 16 | 2048 | 1.3B |
| GPT-3 175B | 96 | 96 | 12288 | 175B |

In your config file:

```python
# config/train_gpt3_small.py
n_layer = 12
n_head = 12
n_embd = 768
block_size = 2048       # GPT-3 uses 2048 context
batch_size = 512
learning_rate = 6e-4
max_iters = 300000
dataset = 'fineweb'
```

### Step 4 — Launch Training

Single GPU:

```bash
python train.py config/train_gpt3_small.py
```

Multi-GPU (recommended for 100B tokens):

```bash
torchrun --standalone --nproc_per_node=8 train.py config/train_gpt3_small.py
```

To reproduce GPT-2 (124M) you'll want at least an 8x A100 40GB node. For GPT-3 scale, you'll need more — typically multiple nodes.

### Step 5 — Alternative: Use Karpathy's nanochat (2025)

Karpathy's nanochat project is an open-source LLM coded in roughly 8,000 lines of PyTorch. It introduces key features such as supervised fine-tuning (SFT), reinforcement learning (RL), and enhanced inference. The training pipeline employs quality data such as FineWeb-EDU for pretraining.

A ~$300 run (12 hours) creates a model better than GPT-2. A ~$1000 run (~42 hours) produces a model with noticeably better reasoning and coherence.

### Step 6 — Evaluate

Standard benchmarks for GPT-3 reproductions:

- **HellaSwag** (commonsense reasoning)
- **MMLU** (knowledge)
- **ARC** (science QA)
- **WinoGrande** (coreference)

Use the `lighteval` or `lm-evaluation-harness` library to run these automatically.

---

## Summary

| Aspect | Detail |
| --- | --- |
| 100B tokens vs full FineWeb | ~0.67% of 15T total — a practical research subset |
| Is it expected? | Yes, typical for a planning script targeting a manageable chunk |
| Best training framework | Karpathy's `build-nanogpt` or `nanochat` |
| Recommended starting size | GPT-3 Small (125M) → needs ~8x A100s, ~$10–$100 |
| Full GPT-3 (175B) | Needs hundreds of A100s + weeks — not practical for individuals |

---

**References:**

- [FineWeb on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [FineWeb Paper (arxiv)](https://arxiv.org/pdf/2406.17557)
- [Karpathy's build-nanogpt](https://github.com/karpathy/build-nanogpt)
- [Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT)
- [nanochat Tutorial](https://www.analyticsvidhya.com/blog/2025/10/andrej-karpathys-nanochat/)
- [FineWeb-Edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
