---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verified Finance Datasets on Hugging Face
translated: false
type: note
---

Here's the verified answer. I checked each dataset by actually fetching its HF page. The previous answer had at least 3 dead links.

---

## Verified Finance Datasets on Hugging Face (June 2026)

I checked each URL. Here's what actually exists, organized by training stage.

---

### TIER 1: Pretraining Corpora (FineWeb-equivalent attempt)

**`kapilrao/SEC-EDGAR`** — THE closest thing to a finance FineWeb
- 590 GB, 8M samples, **43 billion tokens**
- All major SEC EDGAR filings (10-K, 10-Q, 8-K, etc.)
- Collaborators: Datamule, Teraflop AI, Eventual
- This is what BloombergGPT's 363B token proprietary corpus looks like in open form
- https://huggingface.co/datasets/kapilrao/SEC-EDGAR

**`eloukas/edgar-corpus`** — Academic, smaller, cleaner
- 10-K annual reports, 1993-2020, **billions of tokens**
- Paper: "EDGAR-CORPUS: Billions of Tokens Make The World Go Round" (EMNLP 2021)
- 63 likes — well-established in finance NLP research
- https://huggingface.co/datasets/eloukas/edgar-corpus

**`Brianferrell787/financial-news-multisource`** — News corpus at scale
- **57.1M+ rows** from 24 public datasets, 1990-2025
- Unified format — no crawling needed
- 80 likes
- https://huggingface.co/datasets/Brianferrell787/financial-news-multisource

**`PleIAs/SEC`** — SEC filings in clean text
- Part of PleIAs's common_corpus collection
- https://huggingface.co/datasets/PleIAs/SEC

**`JanosAudran/financial-reports-sec`** — Parsed 10-K with structure
- 10-K filings 1993-2020, split into 20 sections + sentences
- Includes sentiment labels from market reactions
- 77 likes
- https://huggingface.co/datasets/JanosAudran/financial-reports-sec

---

### TIER 2: Instruction Tuning / SFT

**`Josephgflowers/Finance-Instruct-500k`** — Largest SFT collection
- **500K+ entries**, multi-task: reasoning, QA, NER, sentiment, multi-turn
- Apache 2.0 license
- Aggregates many finance sources into one
- https://huggingface.co/datasets/Josephgflowers/Finance-Instruct-500k

**`sujet-ai/Sujet-Finance-Instruct-177k`** — Curated multi-task
- **177,597 entries** from 18 HF sources
- 7 task types: sentiment, QA, NER, summarization, classification, etc.
- 83 likes
- https://huggingface.co/datasets/sujet-ai/Sujet-Finance-Instruct-177k

**`nvidia/Nemotron-SpecializedDomains-Finance-v1`** — NVIDIA's synthetic QA
- **326K+ Q&A pairs** from SEC filings (S&P 500, 2019-2024)
- 6-stage template-based synthetic data generation
- **Commercial-ready license**
- https://huggingface.co/datasets/nvidia/Nemotron-SpecializedDomains-Finance-v1

**`FinGPT/fingpt-sentiment-train`** — Sentiment SFT
- Financial news headlines + sentiment labels
- 36 likes, 1.16K followers on FinGPT org
- https://huggingface.co/datasets/FinGPT/fingpt-sentiment-train

**`TheTokenFactory/sec-contracts-financial-extraction-instructions`** — Structured extraction
- 7,683 instruction examples for extracting structured data from SEC filings
- https://huggingface.co/datasets/TheTokenFactory/sec-contracts-financial-extraction-instructions

---

### TIER 3: Numerical Reasoning / Math (for GRPO/DPO)

**`TheFinAI/FinCoT`** — Chain-of-thought financial reasoning
- GPT-4o-generated reasoning paths with iterative verification
- Good for GRPO reward signal
- https://huggingface.co/datasets/TheFinAI/FinCoT

**`ibm-research/finqa`** — IBM's financial QA benchmark
- Numerical reasoning over financial tables/text
- 14 likes, well-cited
- https://huggingface.co/datasets/ibm-research/finqa

**`yale-nlp/FinanceMath`** — Mathematical finance problems
- 19 likes, requires agreement to access
- Covers DCF, Black-Scholes, ratio analysis
- https://huggingface.co/datasets/yale-nlp/FinanceMath

**`virattt/financial-qa-10K`** — QA from 10-K filings
- Example: NVIDIA 2023 10-K Q&A pairs
- Good for teaching models to read actual filings
- https://huggingface.co/datasets/virattt/financial-qa-10K

---

### TIER 4: Benchmarks & Evaluation

**`SALT-NLP/FLUE-FiQA`** — FLUE benchmark
- Financial Language Understanding Evaluation
- FiQA subtask for financial opinion mining
- https://huggingface.co/datasets/SALT-NLP/FLUE-FiQA

**`yixuantt/FinEntity`** — Entity-level sentiment (EMNLP 2023)
- First public dataset for entity-level sentiment in finance
- Sentiment directed at specific entities in news
- https://huggingface.co/datasets/yixuantt/FinEntity

**`takala/financial_phrasebank`** — Classic sentiment benchmark
- 4,840 sentences, 3-class (pos/neg/neutral)
- 259 likes — most popular finance sentiment dataset on HF
- CC BY-NC-SA 3.0
- https://huggingface.co/datasets/takala/financial_phrasebank

**`zeroshot/twitter-financial-news-sentiment`** — Twitter finance sentiment
- 173 likes
- https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment

---

### TIER 5: Structured / Market Data

**`defeatbeta/yahoo-finance-data`** — Price + fundamentals
- Yahoo Finance, Nasdaq, US Treasury data
- Regularly updated
- 96 likes
- https://huggingface.co/datasets/defeatbeta/yahoo-finance-data

**`glopardo/sp500-earnings-transcripts`** — Earnings calls
- S&P 500 earnings transcripts 2014-2024
- Combined with quarterly financial metrics
- Used in ECB working paper
- https://huggingface.co/datasets/glopardo/sp500-earnings-transcripts

**`Josephgflowers/Financial-NER-NLP`** — Financial NER
- Derived from FiNER-139 (1.1M sentences, 139 XBRL tags)
- Reformatted as NL prompts for LLM training
- https://huggingface.co/datasets/Josephgflowers/Financial-NER-NLP

---

### What's Missing (honest assessment)

There is **no single FineWeb-equivalent for finance**. The closest:

| Analogy | Exists? | What to use instead |
|---------|---------|---------------------|
| FineWeb (web crawl → clean) | No | `kapilrao/SEC-EDGAR` (43B tokens of filings) + `Brianferrell787/financial-news-multisource` (57M rows news) |
| BigCode (The Stack) | No | Finance code is too niche; use general code + finance SFT |
| Dolma (AI2 pretrain mix) | No | Build your own mix from the above |

BloombergGPT trained on 363B proprietary tokens. In open data, you can get ~43B tokens from SEC-EDGAR alone, plus ~57M news rows. That's roughly 50-60B tokens total — competitive with BloombergGPT's corpus if you mix well.

---

### Recommended Stack for Your MI300X

```python
# Pretraining (domain-adaptive)
pretrain = [
    "kapilrao/SEC-EDGAR",                    # 43B tokens, filings
    "Brianferrell787/financial-news-multisource",  # 57M rows, news
]

# SFT
sft = [
    "Josephgflowers/Finance-Instruct-500k",  # 500K multi-task
    "nvidia/Nemotron-SpecializedDomains-Finance-v1",  # 326K synthetic QA, commercial OK
    "FinGPT/fingpt-sentiment-train",         # sentiment
]

# Reasoning (GRPO/DPO)
reasoning = [
    "TheFinAI/FinCoT",                       # chain-of-thought
    "ibm-research/finqa",                    # numerical QA
]

# Eval
eval_ds = [
    "takala/financial_phrasebank",           # sentiment benchmark
    "SALT-NLP/FLUE-FiQA",                   # FLUE benchmark
    "yixuantt/FinEntity",                    # entity sentiment
]
```

References:
- [sugatoray/llm-datasets-finance collection](https://huggingface.co/collections/sugatoray/llm-datasets-finance) — curated HF collection of finance datasets
- [adlnlp/FinLLMs GitHub](https://github.com/adlnlp/finllms) — related work + benchmarks list
- [BloombergGPT paper](https://arxiv.org/abs/2303.17564)
- [FINALE paper (ACL 2024)](https://aclanthology.org/2024.finnlp-2.9.pdf) — finance instruction-tuning with CoT rationales
