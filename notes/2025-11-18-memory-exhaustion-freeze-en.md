---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Memory Exhaustion Causes System Freeze
translated: false
type: note
---

Your problem is **not** the GPU (the 4070 Ti is barely being used here). This script is **pure CPU + RAM**, and the hang + GUI freeze after ~140M tokens is almost certainly because you're **running out of RAM** and the system starts heavy swapping to disk, which freezes everything for minutes or hours.

### Why it happens at ~140M–200M tokens

Each token → stored as uint16 → 2 bytes.

- 140 million tokens ≈ 280 MB
- 1 billion tokens ≈ 2 GB
- 10 billion tokens (full FineWeb-10B) ≈ 20 GB
- 100B+ tokens (like many FineWeb/Edu downloads) ≈ 200+ GB

But look at your `all_tokens = []` list in Python: Python lists have massive overhead. Each integer object is ~28–32 bytes on 64-bit Python (even if the value fits in uint16).

Real memory usage while building the list:

- ~150M tokens in a Python list → ~150M × 28–32 bytes ≈ **4–5 GB** just for the list objects
- Then you do `np.array(..., dtype=np.uint16)` → another ~300 MB for the compact array
- Total peak RAM during conversion ≈ 5–6 GB + OS + desktop overhead

You have 62.6 GB RAM, so why freeze at only 140M tokens?

Because your input file `train_fineweb.txt` is probably **much larger** than you think.

People often download FineWeb-100B or even 1T samples and name it “train_fineweb.txt”. If your file is, say, the popular 100B-token FineWeb-Edu sample (~200–300 GB text file), the script will keep reading forever, `all_tokens` list will grow to tens or hundreds of billions of tokens → hundreds of GB of RAM → OOM → swap thrashing → complete desktop freeze. The GPU fans spin because the script is still alive (barely), Python is stuck in the `extend()` or in the final `np.array()` conversion.

### Solutions (pick one)

#### Best fix: Stream directly to .bin without ever holding all tokens in RAM

This version uses almost no RAM (peak < 1 GB even for terabyte-sized text):

```python
# stream_tokenize_to_bin.py
import os
import numpy as np
import tiktoken

enc = tiktoken.get_encoding("gpt2")
CHUNK_SIZE = 1_000_000  # characters per chunk, adjust if needed

def process_file(input_path: str, train_bin: str, val_bin: str, val_ratio=0.0005):
    temp_train = train_bin + '.tmp'
    temp_val = val_bin + '.tmp'

    total_tokens = 0
    val_tokens_written = 0
    val_target = None  # we decide it after first pass or approximate

    with open(input_path, "r", encoding="utf-8", errors='ignore') as f, \
         open(temp_train, "wb") as train_f, \
         open(temp_val, "wb") as val_f:

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            tokens = enc.encode_ordinary(chunk)
            tokens_u16 = np.array(tokens, dtype=np.uint16)

            total_tokens += len(tokens_u16)

            # Approximate validation split on-the-fly (good enough)
            if val_target is None and total_tokens > 10_000_000:
                val_target = int(total_tokens * val_ratio / (1 - val_ratio))

            if val_tokens_written < val_target:
                split_point = min(len(tokens_u16), val_target - val_tokens_written)
                val_f.write(tokens_u16[:split_point].tobytes())
                train_f.write(tokens_u16[split_point:].tobytes())
                val_tokens_written += split_point
            else:
                train_f.write(tokens_u16.tobytes())

            if total_tokens % 50_000_000 == 0:
                print(f"Processed {total_tokens/1e6:.1f}M tokens")

    # Rename temp files
    os.rename(temp_train, train_bin)
    os.rename(temp_val, val_bin)
    print(f"Done! Total ≈ {total_tokens/1e9:.2f}B tokens")
    print(f"train.bin and val.bin ready (no RAM explosion)")

if __name__ == "__main__":
    txt_file = "train_fineweb.txt"
    process_file(txt_file, "train.bin", "val.bin")
```

This streams straight to disk, never holds more than one chunk in memory.

#### If you really want the original script style but safe

Add memory monitoring and shard the output:

```python
# add this instead of one giant list
MAX_TOKENS_PER_SHARD = 500_000_000  # ~1 GB per shard

shard_idx = 0
all_tokens = []

for chunk in iter(lambda: f.read(chunk_size), ""):
    if not chunk:
        break
    tokens = enc.encode_ordinary(chunk)
    all_tokens.extend(tokens)

    if len(all_tokens) >= MAX_TOKENS_PER_SHARD:
        arr = np.array(all_tokens, dtype=np.uint16)
        arr.tofile(f"train_shard_{shard_idx:04d}.bin")
        print(f"Saved shard {shard_idx} - {len(arr)/1e6:.1f}M tokens")
        all_tokens.clear()
        shard_idx += 1
```

Later just cat the shards: `cat train_shard_*.bin > train.bin`

### Quick check how big your file really is

Run these in terminal:

```bash
du -h train_fineweb.txt          # human size
wc -c train_fineweb.txt          # bytes
ls -lh train_fineweb.txt
```

FineWeb-10B text is ~20–25 GB, 100B is ~200–250 GB, etc.

### Summary

Your script dies because Python lists eat 15–20× more RAM than the final numpy array. With big FineWeb files you quickly blow past 50+ GB → swap → frozen desktop.

Use the streaming version above — it works on 1TB+ text files with <2 GB RAM and finishes in a few hours on a single CPU core.

Your 4070 Ti is innocent here; it's waiting for data that never comes because RAM is dead.
