---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download Shards Script and Usage
translated: false
type: note
---

Added `scripts/download_shards.py` and committed. Here's how to get the real shards and run your exact command with `python3.12`:

## Download the two shards
```bash
cd /mnt/data/bilingual-gpt

# EN: fineweb-edu, sample/10BT shard #0
python3.12 -m scripts.download_shards --source en --out fineweb_edu_shard.jsonl

# ZH: fineweb-2, cmn_Hani train shard #0
python3.12 -m scripts.download_shards --source zh --out fineweb2_cmn_shard.jsonl
```

## Then your command works verbatim
```bash
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.5 --out mixed.txt
```

## What the script supports
- **Presets** — `--source en` / `--source zh` / `--source zh-csg` (opencsg/chinese-fineweb-edu-v2). These were verified against HF today:
  - `en` → `HuggingFaceFW/fineweb-edu :: sample/10BT/000_00000.parquet`
  - `zh` → `HuggingFaceFW/fineweb-2 :: data/cmn_Hani/train/000_00000.parquet` (auto-picks `train`, not `test`)
  - `zh-csg` → `opencsg/chinese-fineweb-edu-v2 :: data/00000.parquet`
- **Manual** — `--repo SomeOrg/ds --file data/x.parquet`
- **Generic parse** — handles `.parquet` (pyarrow), `.jsonl`, and `.jsonl.zst`; extracts the `text` column and writes standard `{"text": ...}` jsonl.
- **`--index N`** — grab the Nth shard (FineWeb-2 cmn_Hani has 370, FineWeb-Edu 10BT has 14).
- **`--limit N`** — cap rows for a quick smoke test before committing to a full download.

I verified:
- discovery resolves the correct shard for all three presets (no download needed),
- the parquet→jsonl conversion works end-to-end with correct UTF-8 (Chinese preserved as raw chars) on a local test parquet.

Two notes:
- All needed deps (`huggingface_hub 1.18.0`, `pyarrow 25.0.0`, `pandas 3.0.5`, `zstandard`) are already installed for `python3.12`, so no install needed. They're now listed in `requirements.txt` too.
- A FineWeb shard is a full downloaded parquet; for a first run try `--limit 5000` to confirm the whole chain before pulling a large file.

Want me to add a `download + mix` convenience script (one invocation pulls the right shards, mixes, and reports the token ratio)?