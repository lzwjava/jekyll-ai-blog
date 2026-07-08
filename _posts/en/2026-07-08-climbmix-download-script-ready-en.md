---
audio: false
generated: true
image: false
lang: en
layout: post
title: ClimbMix Download Script Ready
translated: false
type: note
---

The download script is ready. Here's a summary:

**Created `/home/xiaoxin/projects/zz/climbmix/download.py`** — parallel downloader for `nvidia/Nemotron-ClimbMix`

Supports three subsets:

| Option | Files | Approx Size |
|--------|-------|-------------|
| `--subset small` (default) | 100 parquet shards in `climbmix_small/` | ~50 GB |
| `--subset main` | 100 tokenized JSONL files (`part_0..part_99`) | ~2 TB |
| `--subset full` | both of the above + extras | ~2 TB |

Features:
- Parallel downloads via `ThreadPoolExecutor` (default 8 workers, configurable with `--workers N`)
- Resume support via `wget -c` — safe to re-run if interrupted
- Progress stats (MB/s, ETA, cached/error counts)
- `--shard-range LO-HI` to download a specific index range (e.g. `--subset small --shard-range 0-4`)
- `HF_HUB_ENABLE_HF_TRANSFER=1` for 2-5x faster per-stream speeds
- Creates parent directories automatically for subfolder paths like `climbmix_small/`

Example usage:
```bash
# Small subset (smoke test, ~50 GB)
python3 climbmix/download.py --subset small

# Main dataset, shards 10-19 only
python3 climbmix/download.py --subset main --shard-range 10-19 --workers 16

# Full dataset with hf_transfer
HF_HUB_ENABLE_HF_TRANSFER=1 python3 climbmix/download.py --subset full --workers 16
```

The small subset is already in parquet format with a `text` column, ready for tokenization. The main dataset files are `.tokenized.jsonl` (LFS) and need `detokenize_climbmix.py` to convert back to readable text.