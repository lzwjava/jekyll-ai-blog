---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Tokenized FineWeb Sharding Script
translated: false
type: note
---

New script at `scripts/extract/tokenize_fineweb_gpt3.py`. Original `extract_fineweb_gpt3.py` untouched.

**What it does**
- Streams parquet shards via `pq.iter_batches` (same memory profile as the fixed extract script — flat RSS).
- Tokenizes with GPT-2 BPE through `multiprocessing.Pool` (defaults to `cpu_count//2` workers, chunksize 16).
- Each document prefixed with the `<|endoftext|>` token id (50256) as the integer, not as literal text — fixes a subtle issue in the old `.txt` pipeline where the separator was being re-tokenized as characters.
- Packs into 100M-token uint16 shards, `np.save`'d as `edufineweb_val_000000.npy` (first shard) and `edufineweb_train_NNNNNN.npy` (rest) — exact filename pattern `nanoGPT/data/fineweb/prepare_fineweb.py` produces, so the training loader works unchanged.

**Output**
- Default dir: `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B/`
- Overridable via `--input-dir`, `--output-dir`, `--shard-size`, `--nprocs`.

**Run it**
```
python3.11 scripts/extract/tokenize_fineweb_gpt3.py
```

**Caveats**
- No mid-run resume — if it dies, it restarts from shard 0 (will warn and overwrite). Tell me if you want resumability and I'll add a `--start-doc` offset or shard-skip.
- Tokenization is CPU-bound; on this 62 GB box with `os.cpu_count()//2` workers expect roughly an order of magnitude faster end-to-end than the text-file path (and no terabytes of intermediate disk).