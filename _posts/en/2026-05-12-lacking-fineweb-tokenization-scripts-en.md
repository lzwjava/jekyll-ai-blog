---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lacking FineWeb Tokenization Scripts
translated: false
type: note
---

Short answer: **no — there is no tokenization script in this repo.** Only download + parquet→text extraction exists.

What's here today (`scripts/`):
- `download/` — fetches FineWeb parquet shards (and Wikimedia dumps)
- `extract/extract_fineweb.py` — concatenates parquet rows into a single `.txt`, inserting `<|endoftext|>` separators (datasets/fineweb-edu/ already holds the raw parquet shards)
- `analysis/` — log/eval helpers
- no `prepare.py`, no `tiktoken`/`uint16` writer, no `train.bin`/`val.bin` output

**Before handing data to nanoGPT you need to:**

1. Concatenate parquets to text with EOT delimiters → already covered by `extract_fineweb.py` (but it points at `fineweb_test_dump/`, not `datasets/fineweb-edu/`).
2. Tokenize that text with GPT-2 BPE (`tiktoken.get_encoding("gpt2")`), append the `<|endoftext|>` id between docs.
3. Write the token ids as `np.uint16` into a flat `train.bin` / `val.bin` (this is the format `nanoGPT/train.py` memmaps via `data/<name>/{train,val}.bin`).

The canonical reference is nanoGPT's `data/openwebtext/prepare.py` — it streams the HF dataset, tokenizes with tiktoken in parallel, and dumps `train.bin`/`val.bin`. We'd want a `scripts/extract/prepare_fineweb_edu.py` that does the same but reads the local parquet shards in `datasets/fineweb-edu/` instead of pulling from HF.

Want me to write that prepare script (parquet shards → `train.bin` + `val.bin` with GPT-2 BPE)?