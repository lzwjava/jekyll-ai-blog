---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Finance Datasets on Hugging Face
translated: false
type: note
---

**Question:** What are the best finance-domain datasets on Hugging Face for training LLMs, analogous to BigCode for code or FineWeb for general text?

**Answer:**

## Finance Datasets on Hugging Face — Tiered by Use Case

### Tier 1: Large-Scale Pretraining Corpora

**[financial-datasets/financial-reports](https://huggingface.co/datasets/financial-datasets/financial-reports)**
- SEC filings (10-K, 10-Q, 8-K), earnings call transcripts
- Good for domain-adaptive pretraining on formal financial language

**[Sujet-Finance/Sujet-Finance-Instruct-177k](https://huggingface.co/datasets/Sujet-Finance/Sujet-Finance-Instruct-177k)**
- 177K instruction pairs covering sentiment, QA, NER, summarization
- Finance-specific instruction tuning

**[TheFinAI/Fino1_Reasoning_Path](https://huggingface.co/datasets/TheFinAI/Fino1_Reasoning_Path)**
- Chain-of-thought reasoning traces on financial problems
- Good for GRPO/DPO on numerical reasoning

---

### Tier 2: Task-Specific SFT Data

| Dataset | Size | Use Case |
|---|---|---|
| `zeroshot/twitter-financial-news-sentiment` | ~11K | Sentiment (FinSentiment) |
| `nickmuchi/financial-classification` | ~5K | News classification |
| `FinGPT/fingpt-sentiment-train` | ~76K | Sentiment SFT (FinGPT style) |
| `FinGPT/fingpt-forecaster` | ~200K | Price movement prediction |
| `FinGPT/fingpt-fiqa_qa` | ~17K | Financial QA (FiQA) |
| `TheFinAI/flare-fiqasa` | ~1K | Few-shot QA benchmark |

FinGPT org has the most complete SFT collection: `huggingface.co/FinGPT`

---

### Tier 3: Raw Financial Text (for Pretraining)

**SEC EDGAR full-text** — not on HF directly, but:
```bash
# Edgar full-text search bulk download
wget https://efts.sec.gov/LATEST/search-index?q=%22%22&dateRange=custom&startdt=2020-01-01&enddt=2024-01-01&_source=file_date,period_of_report,entity_name,file_num,form_type&hits.hits._source=true
```

Better: use the `edgartools` Python lib:
```bash
pip install edgartools
```
```python
from edgar import Company
c = Company("AAPL")
filings = c.get_filings(form="10-K")
text = filings[0].obj().text  # raw 10-K text
```

**[eloukas/edgar-corpus](https://huggingface.co/datasets/eloukas/edgar-corpus)**
- 6,500+ 10-K annual reports (2000–2020)
- ~250M tokens of formal SEC prose

---

### Tier 4: Numerical / Quantitative Finance

**[TheFinAI/flare-sm-acl18](https://huggingface.co/datasets/TheFinAI/flare-sm-acl18)**
- Stock movement prediction with news headlines + price direction

**[luqia/FinanceMath](https://huggingface.co/datasets/luqia/FinanceMath)**
- Mathematical finance word problems with solutions
- Good for teaching models to do DCF, Black-Scholes, etc.

---

### What BigCode → Finance Looks Like

BigCode's value was **scale + dedup + quality filtering**. Finance doesn't have an equivalent yet. The closest analog being built:

- **FinPile** (paper, not public yet) — 1.3B token finance corpus
- **BloombergGPT trained on** 363B token proprietary corpus — their data never released

So the honest answer: **there's no FineWeb equivalent for finance**. You'd need to build it from:

```
EDGAR 10-K/10-Q/8-K (eloukas/edgar-corpus)     ~250M tokens
Earnings call transcripts (Motley Fool, SA)       ~100M tokens
Financial news (Reuters, Bloomberg headlines)     ~50M tokens
Financial textbooks / CFA materials (PDF scrape)  ~20M tokens
FinGPT SFT data (for alignment)                  ~500K pairs
```

---

### Recommended Pipeline for Your Setup

Given your MI300X and training experience with nanoGPT:

```python
# Quick domain-adaptive pretraining stack
datasets = [
    "eloukas/edgar-corpus",           # pretraining backbone
    "FinGPT/fingpt-sentiment-train",  # SFT layer
    "TheFinAI/Fino1_Reasoning_Path",  # reasoning traces for GRPO
]

# Load and mix
from datasets import load_dataset, interleave_datasets

edgar = load_dataset("eloukas/edgar-corpus", split="train")
fingpt = load_dataset("FinGPT/fingpt-sentiment-train", split="train")

mixed = interleave_datasets([edgar, fingpt], probabilities=[0.8, 0.2])
```

For a bank AI use case (your context): lean heavy on EDGAR + earnings calls for pretraining, then SFT on FinGPT sentiment/QA, then DPO/GRPO on Fino1 reasoning traces. That's the closest to a production-grade finance LLM stack available in open data today.

**References:**

- [FinGPT datasets on HuggingFace](https://huggingface.co/FinGPT)
- [eloukas/edgar-corpus](https://huggingface.co/datasets/eloukas/edgar-corpus)
- [TheFinAI/Fino1_Reasoning_Path](https://huggingface.co/datasets/TheFinAI/Fino1_Reasoning_Path)
- [Sujet-Finance-Instruct-177k](https://huggingface.co/datasets/Sujet-Finance/Sujet-Finance-Instruct-177k)
- [BloombergGPT paper](https://arxiv.org/abs/2303.17564)
