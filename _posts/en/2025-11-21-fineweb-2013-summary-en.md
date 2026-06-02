---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: FineWeb 2013 Dataset Summary
translated: false
type: note
---

**CC-MAIN-2013-20** (Summer 2013 dump) in the FineWeb dataset:

- **Number of .parquet files**: Approximately **460–500**
  (Files are sharded with varying sizes: many ~1 GB, some larger up to ~2 GB. The directory totals **422 GB**, so 422 ÷ ~0.9 GB average ≈ 460–480 shards. The naming is sequential `000_00000.parquet` to roughly `000_004xx.parquet`.)

- **Total size of all parquet files**: **422 GB**

- **Tokens when encoded with a GPT-style tokenizer** (cl100k_base used for GPT-4, or the older GPT-2 tokenizer used in FineWeb reporting):
  **144.5 billion tokens** (after FineWeb's cleaning, filtering, and deduplication pipeline)

Note: The original raw Common Crawl dump was much larger (~393 billion tokens before filtering), but FineWeb keeps only the high-quality English text, which is why this old 2013 dump shrinks so dramatically.

If you download the entire directory (e.g. via `huggingface-cli download` or a script that loops over all shards), you’ll end up with ~422 GB of parquet files containing 144.5B tokens ready for training.

[FineWeb dataset card (includes per-dump token table)](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
[CC-MAIN-2013-20 directory on HF (shows total size)](https://huggingface.co/datasets/HuggingFaceFW/fineweb/tree/main/data/CC-MAIN-2013-20)
