---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flexible Dataset Download and Planning Script
translated: false
type: note
---

Added `scripts/download/plan_and_download_fineweb.py`. What it does that the existing scripts don't:

- **Tokens, not shards.** You give it `--target-tokens 10B` (or `300B`, `1T`); it picks the right number of shards.
- **Whole dataset, not just CC-MAIN-2013-20.** Uses `HfApi.repo_info` to enumerate every parquet file in the repo, then filters to `--dump CC-MAIN-2024-10` if you want one snapshot.
- **FineWeb or FineWeb-Edu** via `--dataset fineweb-edu` (the high-quality 1.3T-token subset you mentioned).
- **`--plan` mode** that prints shard count, total bytes, estimated tokens, dumps covered, then exits — so you can size up before burning bandwidth.
- **Resumable downloads** (HTTP `Range` header + `.part` file), `--mirror hf-mirror` for Asia, progress + MB/s + ETA.

Quick examples:

```bash
# See the plan for 10B tokens of FineWeb-Edu, no download
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb-edu --target-tokens 10B --plan

# Pull 100B tokens via the mirror into datasets/
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb-edu --target-tokens 100B \
    --output-dir datasets/fineweb-edu --mirror hf-mirror

# Single snapshot only, GPT-2-class experiment
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb --target-tokens 5B --dump CC-MAIN-2024-10
```

Note on the heuristic: token estimates use 4 bytes/token (GPT-2 BPE on English). After you've tokenized your first batch with your actual tokenizer, pass the measured value via `--bytes-per-token` for sharper planning. Also added `huggingface_hub` and `datasets` to `requirements.txt`.
