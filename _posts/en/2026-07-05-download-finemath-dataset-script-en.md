---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download FineMath Dataset Script
translated: false
type: note
---

Created `/home/xiaoxin/projects/zz/finemath/download_finemath.py` — the directory and script are ready.

**Script:** `finemath/download_finemath.py`

Downloads parquet shards from **HuggingFaceTB/finemath** (the 54B-token educational math dataset). Coverage:

| Config | Shards | Size |
|---|---|---|
| `finemath-3plus` | 128 | 60.6 GB |
| `finemath-4plus` | 64 | 17.1 GB |
| `infiwebmath-3plus` | 64 | 43.6 GB |
| `infiwebmath-4plus` | 32 | 17.9 GB |
| **Total** | **288** | **139.2 GB** |

**Usage examples:**
```bash
# See what would be downloaded (dry-run)
python3 finemath/download_finemath.py --plan

# Download only the K-12 math subset (60 GB)
python3 finemath/download_finemath.py --config finemath-3plus

# Download everything (~139 GB)
python3 finemath/download_finemath.py

# Use HF mirror (faster from Asia)
python3 finemath/download_finemath.py --mirror hf-mirror

# Download just 10 GB for testing
python3 finemath/download_finemath.py --target-gb 10 --plan
```

Key features (inherited patterns from the existing `plan_and_download_fineweb.py`):
- **Resumable** — uses `wget -c`, skips already-downloaded shards
- **Mirror support** — `--mirror hf-mirror` for accelerated downloads from Asia
- **Partial download** — `--target-gb N` to grab a subset
- **Progress** — per-shard stats, rate, ETA