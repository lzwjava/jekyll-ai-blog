---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data Migration and FineWeb Extraction Update
translated: false
type: note
---

Done with both steps.

**Move:** `~/projects/nanoGPT` → `/mnt/data/nanoGPT` (26G), with `~/projects/nanoGPT` now a symlink to it. Home recovered ~26G (92% → 89%, 98G free).

**Script:** `/mnt/data/zz/scripts/extract/extract_fineweb_gpt3.py` now reads `/mnt/data/zz/datasets/fineweb-edu/data__*.parquet` (the shards downloaded by `plan_and_download_fineweb_gpt3.py`) and writes `/mnt/data/nanoGPT/data/fineweb/train_fineweb.txt`. Per-row logic is unchanged.

One thing to flag: the existing 16G `train_fineweb.txt` at the output path will be overwritten when you run this. If you'd rather keep the old one as a backup, rename it first (`mv train_fineweb.txt train_fineweb.old.txt`). 

Want me to kick off the extraction now? It'll take a while — there are ~200 parquet shards (~400 GB of compressed parquet) and `df.iterrows()` is slow. If we're committing to a long run, I'd suggest a quick optimization first: switch from `iterrows()` to direct column iteration (~5-10× faster). Your call.