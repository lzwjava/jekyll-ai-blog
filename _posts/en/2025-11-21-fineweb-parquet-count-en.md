---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: FineWeb Dataset Parquet File Count
translated: false
type: note
---

The **FineWeb** dataset (the 15T+ token English version at `HuggingFaceFW/fineweb`) contains **approximately 35,000 to 50,000** `.parquet` files in total.

### Breakdown

- It consists of **96** separate Common Crawl snapshots (dumps, e.g., `CC-MAIN-2013-20`, `CC-MAIN-2024-10`, etc.).
- Each dump is stored in its own subdirectory under `/data/` and split into many sharded `.parquet` files named like `000_00000.parquet`, `000_00001.parquet`, … (zero-padded, sequential).
- The number of parquet files varies per dump depending on its size:
  - Smaller/older dumps (like the `CC-MAIN-2013-20` example in your script) often have **~200–1,000** files.
  - Larger recent dumps can have **several thousand** files each.
- There is no single official published total, but community estimates and calculations from dump sizes/token counts consistently put the **overall total around 35k–50k** parquet files across all 96 dumps (the full dataset is ~45–53 TB uncompressed).

Your script downloads shards 11 through 20 (10 files) from the very small `CC-MAIN-2013-20` dump, which has far more than that — many hundreds of shards in total for that dump alone.

If you want the exact count, you can compute it programmatically with the Hugging Face Hub API (e.g., using `huggingface_hub.list_repo_files`), but the rough numbers above are what people generally use when downloading or processing the full dataset.

[FineWeb dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
[FineWeb data tree (example dump)](https://huggingface.co/datasets/HuggingFaceFW/fineweb/tree/main/data)
