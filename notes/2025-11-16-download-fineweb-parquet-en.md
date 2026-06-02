---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Download Specific FineWeb Parquet Files
translated: false
type: note
---

You just want to download and use a few parquet files from one Common Crawl dump (like CC-MAIN-2013-20) instead of the whole 15T-token FineWeb monster — totally reasonable! Here’s the easiest ways to do it in 2025.

### Method 1: Direct Download with huggingface_hub (Recommended, Fastest)
This downloads only the parquet files you want at full speed (~GB/s if you enable hf-transfer).

```bash
# 1. Install/upgrade
pip install -U "huggingface_hub[hf_transfer]"

# 2. Enable fast download (very important!)
export HF_HUB_ENABLE_HF_TRANSFER=1   # Linux/macOS
# or on Windows PowerShell:
# $env:HF_HUB_ENABLE_HF_TRANSFER = "1"

# 3. Download just a few parquet files you want
huggingface-cli download HuggingFaceFW/fineweb \
    data/CC-MAIN-2013-20/000_00000.parquet \
    data/CC-MAIN-2013-20/000_00001.parquet \
    data/CC-MAIN-2013-20/000_00002.parquet \
    --repo-type dataset --local-dir fineweb-2013-20
```

That’s it — you now have three ~2.15 GB parquet files in the folder `fineweb-2013-20/`.

### Method 2: One-Liner Python Script to Download Specific Files
```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb",
    repo_type="dataset",
    allow_patterns=[
        "data/CC-MAIN-2013-20/000_00000.parquet",
        "data/CC-MAIN-2013-20/000_00001.parquet",
        # add more if you want
    ],
    local_dir="fineweb-2013-20"
)
```

### How to Read the Parquet Files Locally
```python
import pandas as pd
# or use pyarrow for speed + lower memory
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# Fastest way (streams without loading everything in RAM)
dataset = ds.dataset("fineweb-2013-20/data/CC-MAIN-2013-20/", format="parquet")

for batch in dataset.to_batches(batch_size=1024):
    df = batch.to_pandas()
    for text in df["text"]:
        # do whatever you want: tokenize, filter, write to jsonl, etc.
        print(text[:200])  # example
```

Or simply with pandas (fine for a few files):
```python
df = pd.read_parquet("fineweb-2013-20/data/CC-MAIN-2013-20/000_00000.parquet")
print(df.columns)  # ['text', 'id', 'dump', 'url', 'date', 'file_path', 'language', 'language_score', 'token_count']
print(df.iloc[0]["text"])
```

### Quick Stats for CC-MAIN-2013-20
- ~207 parquet files × ~2.15 GB ≈ 422 GB total
- ~44 billion tokens (good size for small-to-medium experiments)
- Already cleaned, deduplicated, and filtered by Hugging Face

That’s all you need. Just pick however many `_0000XX.parquet` files you want (they’re shuffled), download only those, and start training or filtering right away.
