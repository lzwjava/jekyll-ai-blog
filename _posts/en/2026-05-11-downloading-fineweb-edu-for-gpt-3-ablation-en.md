---
audio: false
generated: true
image: false
lang: en
layout: post
title: Downloading FineWeb-Edu for GPT-3 Ablation
translated: false
type: note
---

Removed the file. Here's the guide:

---

# Downloading 100B Tokens of FineWeb-Edu for a Small-Scale GPT-3 Ablation

A walkthrough of `scripts/download/plan_and_download_fineweb_gpt3.py` — how it plans, downloads, and resumes a ~400 GB pull of FineWeb-Edu from China without a VPN.

## Why 100B tokens

100B tokens is the budget the GPT-3 paper used per token-count ablation in Table 2.1 — large enough to train interesting models, small enough to fit on one workstation. Chinchilla scaling (~20 tokens per parameter) puts 100B tokens at a ~5B-parameter compute-optimal model. For a 1.3B-parameter Chinchilla-fit, you'd want ~26B; 100B is comfortably over-budget for that range, which is what makes it a useful ablation slice.

Cheatsheet (English BPE, ~4 bytes/token):

| budget   | shards   | disk        | notes                              |
| -------- | -------- | ----------- | ---------------------------------- |
| 10B      | ~20      | ~40 GB      | GPT-2-class                        |
| **100B** | **~200** | **~400 GB** | **GPT-3 ablation (this script)**   |
| 300B     | ~600     | ~1.2 TB     | GPT-3 paper's full training set    |
| 1T       | ~2000    | ~4 TB       | Chinchilla-optimal for ~50B params |
| 1.3T     | full     | ~5.4 TB     | Full FineWeb-Edu                   |

## Why FineWeb-Edu

[FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) filters FineWeb by an "educational value" classifier. It's smaller and cleaner than raw FineWeb — better tokens per training step for the kind of benchmarks (MMLU, ARC, HellaSwag) that ablation experiments usually report.

If you want raw web text instead, swap `REPO_ID` to `HuggingFaceFW/fineweb`.

## Why hf-mirror.com

Direct access to `huggingface.co` is unreliable from mainland China. `hf-mirror.com` is a community mirror that serves the same parquet shards over CDN endpoints that aren't blocked. The script:

1. Sets `HF_ENDPOINT=https://hf-mirror.com` **before** importing `huggingface_hub`, so the `HfApi().repo_info()` listing call also goes through the mirror — not just the parquet downloads.
2. Hardcodes `BASE_URL` for the actual file fetches.

If you're outside China, the same script works against the mirror — it just won't be faster than the official endpoint.

## The architecture

Three phases, decoupled:

```
list_parquet_shards()   →   select_shards()   →   download_one() per shard
   (HfApi, once)              (token budget)         (resumable)
```

State lives in `<output-dir>/progress.json`. First run writes it; later runs load it and skip the HF API call entirely.

### `progress.json` shape

```json
{
  "repo_id": "HuggingFaceFW/fineweb-edu",
  "target_tokens": 100000000000,
  "bytes_per_token": 4.0,
  "shards": [
    {"path": "data/CC-MAIN-2013-20/000_00000.parquet", "size": 2147483648,
     "dump": "CC-MAIN-2013-20", "status": "done"},
    {"path": "data/CC-MAIN-2013-20/000_00001.parquet", "size": 2147483648,
     "dump": "CC-MAIN-2013-20", "status": "pending"}
  ]
}
```

Updated atomically (`tmp` + `os.replace`) after every shard finishes, so a SIGKILL or power cut never leaves it half-written.

### How resumption actually works

Two independent layers:

1. **Per-shard** (`.part` file + HTTP `Range: bytes=N-`): if you Ctrl-C while a 2 GB shard is half downloaded, the partial bytes stay in `shard.parquet.part`. Next run sees the `.part`, opens it in append mode, and asks the server for the rest.
2. **Across shards** (`progress.json` status field): finished shards are marked `done`. Next run skips them in O(1) — no `os.path.exists` walk, no re-listing from HF.

Together: you can kill the process at any moment and lose at most the bytes buffered in memory (< 1 MB).

## Usage

```bash
# Dry run — list shards, write progress.json, but don't download
python scripts/download/plan_and_download_fineweb_gpt3.py --plan

# Download (or resume) ~400 GB into datasets/fineweb-edu/
python scripts/download/plan_and_download_fineweb_gpt3.py

# Custom output location
python scripts/download/plan_and_download_fineweb_gpt3.py \
    --output-dir /mnt/data/fineweb-edu

# Discard the saved plan and re-pick from a fresh HF listing
python scripts/download/plan_and_download_fineweb_gpt3.py --refresh-plan
```

On the first run you'll see something like:

```
Listing shards in HuggingFaceFW/fineweb-edu...
Wrote new plan to datasets/fineweb-edu/progress.json.

Plan: ~100,000,000,000 tokens @ 4.0 bytes/token (small-scale GPT-3 ablation):
  shards:        198  (0 done)
  download size: 398.4 GB  (0.0 B already on disk)
  est. tokens:   107,000,000,000
  dumps covered: 1 (CC-MAIN-2013-20)

Downloading to datasets/fineweb-edu via https://hf-mirror.com ...
  [1/198] data/CC-MAIN-2013-20/000_00000.parquet (2.0 GB)
      progress: 2.0 GB / 398.4 GB  18.3 MB/s  ETA 360.1 min
```

Re-running after Ctrl-C:

```
Loaded plan from datasets/fineweb-edu/progress.json (198 shards).

Plan: ~100,000,000,000 tokens @ 4.0 bytes/token (small-scale GPT-3 ablation):
  shards:        198  (47 done)
  download size: 398.4 GB  (94.0 GB already on disk)
  ...
  [1/198] done  data/CC-MAIN-2013-20/000_00000.parquet (2.0 GB)
  ...
  [48/198] data/CC-MAIN-2013-20/000_00047.parquet (2.0 GB)
      attempt 1/3 failed: ...  ← resumes from .part automatically
```

## Things to know before running

- **Disk**: 400 GB free. The shards are not compressed further on disk; one parquet file ≈ one shard ≈ ~2 GB.
- **Bandwidth**: at 20 MB/s sustained from hf-mirror.com, ~5.5 hours. Slower from residential connections.
- **Token estimate is a heuristic**: `bytes / 4.0`. Real tokenizer counts vary ±10–15% depending on whether you use GPT-2 BPE, tiktoken, or SentencePiece. Override `BYTES_PER_TOKEN` if you've measured it.
- **Single CC dump**: FineWeb-Edu's first shards live under `CC-MAIN-2013-20`. 198 shards is more than that snapshot contains, so the plan will span multiple dumps in dump-sorted order. If you want topically-balanced data, randomize the shard selection instead — the current ordering is deterministic but not domain-balanced.
- **Not idempotent against the dataset evolving**: if HuggingFace re-shards FineWeb-Edu, `progress.json` paths can go stale. Use `--refresh-plan` to rebuild.

## What's next

The downloaded parquet files are raw text. To turn them into a training corpus, point `scripts/extract/extract_fineweb.py` at `datasets/fineweb-edu/`. That script streams the parquet `text` column through `pyarrow.iter_batches` without loading whole files into memory.
