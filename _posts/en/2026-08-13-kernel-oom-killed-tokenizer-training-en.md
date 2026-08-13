---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel OOM killed tokenizer training
translated: false
type: note
---

Found it. Your process **wasn't stuck — it was OOM-killed by the kernel**. Here's the evidence from the journal (`journalctl`/dmesg):

```
Aug 13 19:57:28 to kernel: Out of memory: Killed process 32871 (python3.12)
total-vm:88230300kB, anon-rss:60743884kB  (≈ 60 GB RSS)
oom_score_adj:100
```

## Why it died

`ByteLevelBPETokenizer` (the Rust `tokenizers` crate) loads the **entire corpus into RAM** and builds a big in-memory merge structure. Your machine has **62 GiB RAM**, and the process had ballooned to **~60 GB** before the OOM killer stepped in.

The current live run was `--input mixed.txt`, which is **11.4 GB** of text. That's far too big for the trainer's memory model on this box.

The empty `/dev/null`-style log (`tok_train_sample.log`, just 1 byte = `\n`) is a second symptom, not a separate bug: when stdout is redirected to a file, Python block-buffers output, and the `print("training on N file(s)")` was sitting in the buffer, never flushed before the kill.

## What to do

Fit the corpus to memory. The 2 GB sample you already made (`mixed_sample_2gb.txt`) is the right size — 11.4 GB → 60 GB, so 2 GB should land around ~10 GB, comfortable.

```bash
python3.12 -m scripts.train_tokenizer \
    --input mixed_sample_2gb.txt \
    --out-prefix tok_mixed \
    --vocab-size 65536
```

If you must train on the full 11.4 GB, options:

- **Shard it** — train on a handful of `.jsonl` shards (the script already accepts a directory of shards) rather than one giant file.
- **Raise `--min-frequency`** (e.g. `--min-frequency 5`) to shrink the merge table.
- **Lower `--vocab-size`** — memory scales with merge candidates.
- Switch to a streaming trainer (the docstring mentions `nanochat`'s rustbpe / `prepare.py`), which processes in a streaming fashion instead of holding the whole corpus.

Want me to kick off the run on the 2 GB sample and watch it?
