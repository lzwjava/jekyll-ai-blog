---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OOM Crash with Chunking
translated: false
type: note
---

Done. The rewritten `scripts/prepare.py` fixes the OOM crash.

## What was wrong

The old one-shot path did this on a 2 GB input:

- `text = f.read()` → one ~2–4 GB Python `str`
- `ids = tok.encode(text).ids` → a **Python list of ~500M+ `int` objects** (~15–20 GB, since token ids > 256 aren't cached)
- `np.array(ids, dtype=dtype)` walks that giant list → memory spikes again → the OOM-killer terminates the process.

## What the fix does

1. **Chunks the input** (~1 MiB of chars per read), extending each chunk to the next `\n` so it never cuts a control-token line, a multi-byte char, or a doc boundary. BPE merges stay doc-local (negligible accuracy impact — this is how large-scale tokenizers normally chunk).
2. **Converts each chunk's id list to a small `uint16` array immediately** and streams it to a temp file with `arr.tofile()`, so the big Python list is discarded every iteration. Peak RAM is bounded by ~one chunk.
3. **Splits train/val by byte offset** (`split * itemsize`) and stream-copies the ranges into `train.bin` / `val.bin` in 1 MiB blocks — never loads the whole token stream into RAM.
4. Prints progress (`chunks=`, `tokens=`) and cleans up the temp file, including on error.

CLI is unchanged, so your command works as-is:

```bash
python3.12 -m scripts.prepare \
    --input mixed_sample_2gb.txt \
    --tok-prefix tok_mixed \
    --out-dir data \
    --val-frac 0.05
```

Notes:

- vocab is exactly 65536 → `prepare.py` uses **uint16** (its check is `<= 65536`, max id 65535 fits). The trainer's "vocab > 65535" warning is conservative; you're fine.
- It'll overwrite the stale 90 KB `data/train.bin` / `data/val.bin` from the earlier smoke test.
- The same script now also safely handles the full 11 GB `mixed.txt` later if you want to train on everything.
