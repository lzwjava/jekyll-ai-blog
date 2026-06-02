---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data Preparation for nanoGPT Training
translated: false
type: note
---

Based on your updated log, here's the complete picture of what's happening with your "60GB text data":

## The Full Story

You're going through **two distinct phases** of data preparation:

### Phase 1: Raw → Tokenized Shards (Complete)

```
Raw text (60GB) → Tokenized .npy shards (28GB)
├── 149 training shards
├── 1 validation shard
└── Format: NumPy arrays (.npy)
```

### Phase 2: .npy → .bin Conversion (In Progress)

```
Tokenized .npy (28GB) → .bin format for nanoGPT
└── Concatenates all shards into single binary file(s)
```

## Why Two Formats?

| Format | Purpose | Size |
|--------|---------|------|
| `.npy` shards | Parallel tokenization, checkpoint-friendly | 28GB total |
| `.bin` | nanoGPT's native format (memory-mapped) | ~Same size |

## Understanding the 60GB → 28GB Ratio

```
60GB raw text
    ↓ (tokenization)
~48B tokens (40M tokens/sec × 20 min)
    ↓ (binary serialization)
28GB .npy files
    ↓ (conversion)
28GB .bin files
```

**Compression ratio**: ~2.14× (60/28)

- Normal for text tokenization
- BPE tokens average ~0.6-0.8 bytes each
- Your math: 48B tokens × 0.58 bytes = 27.8GB ✓

## What's Left

From your log, you're converting `.npy` to `.bin`:

```python
# The script you're running likely does:
for shard in 150_files:
    data = np.load(shard)      # Load token IDs
    data.astype(np.uint16).tofile(output)  # Write binary
```

## Expected Final Output

- **One or two `.bin` files**:
  - `train.bin` (~27-28GB)
  - `val.bin` (~0.2-0.3GB)
- Ready for nanoGPT training with memory mapping
- No data loss — just format optimization

## Quick Verification

```bash
# Check original raw size
du -sh /raw/data/path/

# Check .npy shards total
du -sh /output/npy_shards/

# After conversion
ls -lh *.bin
```

**Bottom line**: Your 60GB raw text → 28GB tokenized data is correct. The 2.14× compression is normal, and converting to `.bin` is the final step before training. Nothing is being lost — you're just preparing data in the format nanoGPT expects for efficient memory-mapped I/O during training.
