---
audio: false
generated: true
image: false
lang: en
layout: post
title: Strategies for Training Large Language Models
translated: false
type: note
---

**Question:** How should I approach training a GPT-3-scale model — thinking about data collection strategy, how much data is really needed, and what's the most cost-effective way to accumulate 10TB+ without paying for expensive external bandwidth?

**Answer:**

Great thinking, and you're on the right track! Let me break this down clearly across three areas: **how much data you actually need**, **where to get it without crazy bandwidth costs**, and **the practical strategy**.

---

## 1. How Much Data Does a GPT-3-Scale Model Actually Need?

First, let's calibrate expectations with real numbers:

GPT-3's training corpus started at 45TB of compressed plaintext (roughly 90TB uncompressed), but after filtering, the actual training mix was around 570GB total — with CommonCrawl contributing about 400GB of that.

So the key insight is: **raw data volume ≠ effective training data volume**. Massive raw dumps get filtered down dramatically.

For reference: GPT-2 was trained on ~40GB of text, GPT-3 on approximately 500 trillion tokens, and Phi-3 on 3 trillion tokens. A solid order of magnitude target for a serious personal experiment is around 1 trillion tokens.

For your current 60GB experiment — that's actually close to GPT-2 scale territory, which is a reasonable start. Jumping to 10TB of raw data is not unreasonable for GPT-3-class ambitions, but you need to account for heavy filtering reducing it significantly.

---

## 2. Data Quality > Raw Size

A smaller model trained on high-quality open source data can outperform a larger model trained on noisy, poorly curated datasets. The preprocessing pipeline — deduplication, URL filtering, tokenization, contamination detection — often matters more than architectural innovations.

**Key ready-made datasets you should look at instead of raw-crawling everything:**

- **FineWeb-edu** — 1.5 trillion tokens, 9TB compressed — a high-quality educative subset with a great quality-to-size ratio, hosted on Hugging Face (`HuggingFaceFW/fineweb-edu`).
- **The Pile** — 800GB, curated, widely used
- **RedPajama** — 1.2T tokens
- **RefinedWeb** — 5T+ tokens

These are pre-filtered and deduplicated, saving you enormous preprocessing work.

---

## 3. How to Get 10TB Without Expensive Bandwidth

You're right to think carefully about this. Here are the real strategies:

### Option A: Use Pre-existing Open Datasets (Best ROI)
Common Crawl comprises petabytes of raw web data released monthly. GPT-3, LLaMA, OpenLLaMA, and T5 all used it in pre-training. You can download specific monthly snapshots directly from `commoncrawl.org` — they offer free S3 access via AWS, which is the cheapest path.

### Option B: Hugging Face `datasets` Library Streaming
You don't need to download 10TB all at once. Use Hugging Face's streaming API — process data on-the-fly without storing everything locally. This avoids the bandwidth problem entirely for training purposes.

```python
from datasets import load_dataset
ds = load_dataset("HuggingFaceFW/fineweb-edu", streaming=True, split="train")
```

### Option C: VPS / Server with Unlimited Internal Bandwidth (Your DMIT approach)
Your instinct about DMIT is solid for bulk downloading:

- Use a VPS with **unlimited or high-quota internal bandwidth** to download datasets from Hugging Face / Common Crawl S3
- Then transfer to your local machine via **local network / hard drive copy** (no external quota burned)
- For 10TB at ~$10/TB used HDD cost, you're looking at **~$100 in storage hardware**

Used HDDs can be found at around €10/TB on eBay or Amazon — just be cautious about "0-hour usage" claims from resellers, and factor in that some drives may fail in transit.

### Option D: Ask Friends / Research Groups for Direct Drive Copy
100% valid. Academic labs and ML communities often share drives directly for exactly this reason. The ML community around Hugging Face is very collaborative about this.

---

## 4. The Practical Roadmap

| Step | Action |
|---|---|
| **Now (60GB)** | Finish GPT-2 scale experiment, run benchmarks (even simple ones like perplexity on held-out set) |
| **Next (500GB–1TB)** | Download FineWeb-edu subset, clean it, tokenize with BPE |
| **Later (10TB+)** | Use VPS to batch-download Common Crawl snapshots, copy to local drives |
| **Training** | Use Chinchilla scaling laws to match data size to model parameter count |

Scaling laws show that parameter count and dataset size should be scaled proportionally for optimal performance — a 70B model trained on insufficient data underperforms a 7B model trained on properly scaled, high-quality data.

The most important thing right now: **run benchmarks on your 60GB GPT-2 experiment first** before scaling. Even simple perplexity measurements or few-shot task evaluations will tell you if your pipeline is working before you invest in 10TB of data collection.

---

**References:**

- [LLMs Explained Part 2: Data Collection](https://joseparreogarcia.substack.com/p/llms-explained-part-2-data-collection-cleaning)
- [Open-Sourced Training Datasets for LLMs - Kili Technology](https://kili-technology.com/large-language-models-llms/9-open-sourced-datasets-for-training-large-language-models)
- [LLM Training Datasets - glennklockwood.com](https://www.glennklockwood.com/garden/LLM-training-datasets)
- [Foundational LLM Pre-training at Home - Medium](https://medium.com/@adrien_morvan/foundational-llm-pre-training-on-your-hardware-at-home-0dd4f2175ea5)
- [LLMDataHub - GitHub](https://github.com/Zjh-819/LLMDataHub)
- [FineWeb-edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
