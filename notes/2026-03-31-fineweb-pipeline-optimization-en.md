---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing the FineWeb Data Pipeline
translated: false
type: note
---

## 🔍 Detailed Review: FineWeb Pipeline

---

### What Went Wrong (and Why)

**Attempt 1: `datasets` streaming library → OOM killed**

The `load_dataset(..., streaming=True)` promise is misleading. Even in "streaming" mode, the HF `datasets` library:

- Loads the entire Arrow schema into memory
- Buffers decompressed parquet chunks in an internal queue
- Runs a Python iterator with significant per-object overhead

On 1.9GB RAM: wrote 115MB before dying
On 3.8GB RAM: wrote 223MB before dying

**Root cause:** Not the data streaming itself — it's the HF library overhead. The Arrow table representation is memory-hungry even when "streaming."

**Attempt 2: `pd.read_parquet()` → OOM killed**

Reads the entire 2.1GB parquet into a pandas DataFrame. Pandas + Arrow conversion needs ~3-4x the file size in RAM. A 2GB parquet needs ~6-8GB RAM to load. Instant death on 3.8GB.

**Attempt 3: `pyarrow.ParquetFile.read_row_group()` → OOM killed**

Better than full pandas, but `to_pandas()` on a row group still converts the entire chunk to a DataFrame. Row groups in FineWeb are large (~100K+ rows), so same problem.

**Attempt 4: `pyarrow.iter_batches(batch_size=4096)` → ✅ Works**

This is the correct approach. It:

- Streams small RecordBatches (4096 rows at a time)
- Each batch is ~few MB in memory
- Never loads the full parquet into RAM
- Peak memory stays under 500MB

---

### Current State Assessment

| Metric | Value |
|---|---|
| Shards processed | 5 of 21 |
| Text extracted | 13 GB |
| Lines written | 76M |
| Disk used | 18 GB of 77 GB |
| RAM peak | ~500 MB |
| OOM kills | 0 (with iter_batches) |

**Remaining shards (5-20):** 16 × ~2GB = ~32GB parquet → ~42GB text
**Total projected:** ~55GB raw text
**Disk after all shards:** 77GB - 18GB - 32GB download - 42GB text ≈ **tight but feasible** (shards are deleted after extraction)

---

### What Needs to Happen Next

**1. Tokenization (critical missing piece)**

You have 76M lines of raw text. Before training, this needs to become `train.bin` and `val.bin`:

```python
# Token counts from 5 shards:
# ~13GB text ≈ 3-4 billion tokens (GPT-2 BPE)
# Full 21 shards ≈ 12-15 billion tokens
```

The tokenization script needs to:

- Read the text line by line (memory-safe)
- Tokenize with `tiktoken` GPT-2 encoder
- Write to binary `uint16` arrays
- Split 90/10 train/val

**Estimated tokenized size:**

- 5 shards: ~6-8 GB (`train.bin` + `val.bin`)
- 21 shards: ~24-30 GB

**2. Disk space calculation**

| File | 5 shards | 21 shards |
|---|---|---|
| Raw text | 13 GB | 55 GB |
| Tokenized | 7 GB | 28 GB |
| Parquet (temp) | 0 GB (deleted) | 0 GB |
| **Total** | **20 GB** | **83 GB** ⚠️ |

21 shards will **exceed the 77GB disk**. You need to either:

- Tokenize shard-by-shard (download → extract → tokenize → delete text)
- Upgrade to a larger disk
- Use fewer shards (`sample-10BT` uses ~5 shards)

**3. The `sample-10BT` subset is not what's being downloaded**

The parquet shards are from `CC-MAIN-2013-20`, which is the full FineWeb dataset, not the curated `sample-10BT`. For GPT-2 124M training, `sample-10BT` is better:

- Curated quality filtering
- ~10B tokens = right-sized for the model
- No need to download 21 shards

**4. No HF token → rate limiting**

You're downloading anonymously. HF limits unauthenticated downloads to ~1GB/hour. Each 2GB shard takes 2+ hours. Full download = 40+ hours. With a token: ~10x faster.

---

### Recommendations

**Immediate (right now):**

- You have 5 shards / ~13GB / ~3-4B tokens. That's enough to test the full pipeline.
- Don't download more shards yet. Tokenize what you have, verify training works.

**Before full download:**

1. Set up HF token: `huggingface-cli login`
2. Switch to `sample-10BT` subset (curated, right-sized)
3. Write a shard-by-shard pipeline (download → extract → tokenize → cleanup) to stay under disk limit
4. Transfer tokenized `train.bin`/`val.bin` to your RTX 4070 for actual training

**For training:**

- 5 shards (~3-4B tokens) with GPT-2 124M config will produce a decent model
- `max_iters=~12000` at effective batch 524K tokens/iter ≈ 6.3B tokens seen (loops dataset once)
- Matches your previous `train_log_fineweb3.txt` config

---

### Summary

| Issue | Severity | Fix |
|---|---|---|
| HF `datasets` OOM | ✅ Solved | Use `pyarrow.iter_batches` |
| Missing tokenizer | 🔴 Blocker | Write `prepare.py` |
| Wrong subset (full vs sample-10BT) | 🟡 Quality | Use `sample-10BT` for training |
| No HF token | 🟡 Speed | `huggingface-cli login` |
| Disk too small for all shards | 🟡 Capacity | Tokenize shard-by-shard or use fewer shards |
| Config mismatch | 🟡 Correctness | Set `max_iters` based on actual token count |

The hard part (memory-safe extraction) is solved. Everything else is plumbing. Want me to write the tokenizer and wire up the full pipeline?
