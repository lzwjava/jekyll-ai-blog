---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing Tiktoken Multiprocessing Pickle Error
translated: false
type: note
---

Your error is very common when using `datasets.map(..., num_proc>1)` with a custom tokenizer (like the Tiktoken encoder used in nanoGPT’s FineWeb script) — the tokenizer loads the BPE file (`cl100k_base.tiktoken` or similar) and this file handle **cannot be pickled** when sent to subprocesses on Linux (fork-based multiprocessing).

The child processes crash immediately → “One of the subprocesses has abruptly died”.

### Quick Fix (works 99% of the time)

Edit `data/fineweb/prepare.py` and force the tokenization to run in the **main process only**:

```python
# Around line 80-85, find the .map() call and change num_proc=8 → num_proc=1

tokenized = raw_datasets.map(
    tokenize,
    num_proc=1,               # ← change this line (or just delete the argument)
    desc="tokenizing the splits",
)
```

It will be slower (single-core), but it will work reliably. On FineWeb-10B this takes ~30-60 minutes depending on your CPU/disk.

### Better Fix (keep multiprocessing, still fast)

Make the tokenizer load lazily inside the worker process instead of in the global scope.

Replace the current tokenizer creation (around line 40-50) with this pattern:

```python
import tiktoken

# Remove the global encoder = tiktoken.get_encoding("cl100k_base")

def get_encoder():
    """Load tokenizer lazily in each subprocess"""
    return tiktoken.get_encoding("cl100k_base")

def tokenize(example):
    enc = get_encoder()                                   # ← loaded per-process
    ids = enc.encode_ordinary(example["text"])
    ids.append(enc.eot_token)  # or whatever the script does
    return {"ids": ids, "len": len(ids)}
```

Then keep `num_proc=8` (or any number). This way each worker loads its own copy of the .tiktoken file after forking → no pickling issues.

### Even Faster Alternative (recommended for repeated runs)

Pre-download the 10B/100B FineWeb-Edu shards from Hugging Face and use Karpathy’s updated script that works directly on the parquet/arrow files instead of the giant .txt file:

```bash
# Much faster and avoids this bug entirely
python data/fineweb/prepare_fineweb.py --version 10B
# or 100B
```

The new script (added ~2024) uses the official HF dataset and is multiprocessing-safe.

### Summary

| Solution                          | Speed     | Complexity | Recommendation |
|-----------------------------------|-----------|------------|----------------|
| `num_proc=1`                      | Slow      | 1 line     | Quick fix      |
| Lazy encoder inside tokenize()    | Fast      | small edit | Best for .txt  |
| Use new prepare_fineweb.py script | Fastest   | new command| Recommended    |

Pick one and you’ll get past this error immediately. Let me know which route you take and I’ll give you the exact patch if needed!
