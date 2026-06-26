---
audio: false
generated: true
image: false
lang: en
layout: post
title: BigQuery vs Local Tokenization
translated: false
type: note
---

Question: When an LLM does tokenization over large Parquet files, the CPU can hang/stall in some cases. Does BigQuery already handle this kind of large-scale processing for you?

Answer:

Let me separate two distinct things you're conflating, because the answer differs for each.

## 1. The CPU "hang" on large Parquet — what's actually happening

When you tokenize a big Parquet locally and the CPU stalls, it's almost never the tokenizer being slow per se. It's usually one of:

- **Loading the whole Parquet into memory** — `pd.read_parquet()` or `pq.read_table()` materializes everything. A 50GB Parquet on a 16GB machine (your M2 Air) swaps to disk and the process appears to hang. The fix is streaming, not more CPU.
- **Single-threaded tokenization** — HuggingFace `tokenizers` (Rust-backed) is fast and releases the GIL, but if you call it row-by-row in a Python loop you serialize everything onto one core.
- **Row-group materialization** — Parquet is columnar; reading it row-by-row for tokenization fights the format.

The local fix is to stream row-groups and batch-tokenize:

```python
import pyarrow.parquet as pq
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
pf = pq.ParquetFile("big.parquet")

for batch in pf.iter_batches(batch_size=10_000, columns=["text"]):
    texts = batch.column("text").to_pylist()
    enc = tok(texts, truncation=True, max_length=1024)  # batched, Rust, multi-core
    # write enc to shards (np.memmap / .bin) — don't hold in RAM
```

This is the nanoGPT/nanochat `prepare.py` pattern: stream → tokenize in batches → write contiguous `uint16` `.bin` shards. The CPU never hangs because you bound memory by batch, and the Rust tokenizer parallelizes across the batch.

## 2. "Does BigQuery handle that?" — yes, but it solves a *different* problem

BigQuery is a **columnar, distributed OLAP warehouse** (Dremel under the hood). It absolutely solves the "large Parquet won't fit / single CPU stalls" problem — but for **SQL-style transforms**, not for running a tokenizer.

What BigQuery gives you for free:

- **No memory ceiling on your machine** — it's serverless; Google fans the scan across thousands of nodes. A 50GB or 5TB Parquet is irrelevant to local RAM.
- **Columnar pruning** — if you only need the `text` column, it reads only that column's storage, never the rest.
- **Massive parallelism** — the scan/filter/aggregate is sharded automatically.

So if your "tokenization" is something BigQuery SQL can express, the answer is yes, it's handled. And increasingly it *can* be:

- **`ML.GENERATE_TEXT` / `ML.GENERATE_EMBEDDING`** — BigQuery ML can call Vertex AI / Gemini models directly in SQL over a table, batching and parallelizing for you.
- **Remote functions / `ML.PREDICT`** — you can register a model and apply it column-wise.

But there's a sharp boundary: **BigQuery does not run your HuggingFace tokenizer**. There's no native "tokenize this text into GPT-2 BPE IDs" SQL function. If you want *your specific* tokenizer (the one matching the model you're training), you have options:

- **Remote UDF** — wrap your tokenizer in a Cloud Function / Cloud Run endpoint, register it as a BigQuery remote function, call it per-row. BigQuery parallelizes the calls. Works, but network round-trips make it slow and expensive for billions of rows.
- **JS UDF** — pure-JS BPE; impractical for real tokenizers.
- **Export-and-process** — the pragmatic choice: use BigQuery to *filter/dedup/sample* the corpus at warehouse scale, export the clean `text` column to Parquet/JSONL in GCS, then run the streaming tokenizer above on a GPU/CPU box (your MI300X cloud or workstation).

## The practical answer for your training pipeline

For nanoGPT-scale to DeepSeek-v4-scale data prep, the AI-native split is:

1. **BigQuery for the heavy data engineering** — dedup, language filtering, quality scoring, sampling, joining. This is where "won't fit on my machine" dies. Let Dremel eat the TBs.
2. **Stream-tokenize the cleaned output yourself** — because the tokenizer must match your model exactly, and you want contiguous `.bin` shards for fast training data loading. Run it where the CPU cores are (workstation) or on the box next to your GPU.

BigQuery removes the *scale* problem. It does not remove the *tokenizer-fidelity* problem. Don't try to force BPE tokenization into SQL — that's the one piece you keep local/owned, and the streaming-batch pattern above means it never hangs regardless of corpus size.

If you tell me your actual corpus size and which tokenizer/model you're prepping for, I'll give you the exact `prepare.py` with sharding sizes tuned for your MI300X loader.
