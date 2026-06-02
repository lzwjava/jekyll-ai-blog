---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Small High-Quality Dataset Alternatives
translated: false
type: note
---

Yes, OpenWebText is huge (~9B tokens, 17GB uint16 file) and takes a long time to preprocess and a lot of disk space. Here are much smaller high-quality alternatives that are commonly used for testing, debugging, or training small models quickly:

| Dataset                  | Approx. tokens | Final .bin size (uint16) | Why people like it                                                                 | How to get it quickly                                      |
|--------------------------|----------------|--------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------|
| **OpenWebText-10k**      | ~40M           | ~80MB                    | Exact same distribution as full OpenWebText, just first 10k documents             | `load_dataset("openwebtext", split="train[:10k]")`         |
| **OpenWebText-100k**     | ~400M          | ~800MB                   | Still very representative, finishes tokenizing in a few minutes                   | `split="train[:100k]"`                                     |
| **FineWeb-Edu sample**   | 50M–1B         | 100MB–2GB                | Higher quality than OWT (LLama-style filtering), very popular lately              | `load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BQ", split="train")` → ~50M tokens |
| **Shakespeare**          | ~1M            | ~2MB                     | Classic tiny dataset, perfect for quick sanity checks                             | `load_dataset("tiny_shakespeare")` or just download the single .txt file |
| **PG-19 (books)**        | Full 2.8B      | ~5.5GB                   | Very clean public-domain books, but you can take just a slice                      | `load_dataset("pg19", split="train[:5%]")` → ~140M tokens  |
| **C4 (subset)**          | variable       | variable                 | Common Crawl cleaned by T5 team, English only                                      | `load_dataset("allenai/c4", "en", split="train[:1%]")` streaming=True |
| **RedPajama sample**     | 5M–200M        | 10MB–400MB               | Mix of sources (CommonCrawl, Wikipedia, books, etc.), same recipe as LLaMA         | `load_dataset("togethercomputer/RedPajama-Data-1T", name="sample", split="train")` |

### My personal recommendations depending on your goal

1. Just want something that runs in < 5 minutes and fits anywhere → **tiny_shakespeare**
   (nanoGPT users love this one)

2. Want something still “real internet text” but tiny → OpenWebText first 10k documents

   ```python
   dataset = load_dataset("openwebtext", split="train[:10000]")
   ```

3. Want the highest-quality small dataset right now (2025) → FineWeb-Edu 10B-token sample
   (~50M tokens, but much cleaner than OWT, almost identical quality to what top labs use)

   ```python
   dataset = load_dataset(
       "HuggingFaceFW/fineweb-edu",
       name="sample-10BQ",  # 10 billion tokens sampled, ~50M per shard if you slice
       split="train"
   )
   ```

4. Want something < 500MB but still diverse → RedPajama sample (200M tokens version)

   ```python
   dataset = load_dataset("togethercomputer/RedPajama-Data-1T", name="sample-200M", split="train")
   ```

All of these drop into your exact same preprocessing script with zero changes (just replace the load_dataset line).

For quick iteration I usually keep three binaries on disk:

- `shakespeare.bin`   (~2MB)   → overfit tests
- `owt_10k.bin`       (~80MB)  → debugging new code
- `fineweb_edu_1B.bin` (~2GB) → actual small-model training

Let me know how big you want it and I can give you the exact one-liner!
