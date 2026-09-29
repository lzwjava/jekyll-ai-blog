---
audio: false
generated: true
image: false
lang: en
layout: post
title: Largest training text in nanoGPT
translated: false
type: note
---

The largest training **text** file is here in **nanoGPT**, not in nanochat.

## Here — `/mnt/data/nanoGPT`

| File | Size |
|---|---|
| **`data/fineweb/train_fineweb.old.txt`** | **16 GB** ⬅ largest |
| `data/wikipedia_local/train_wikipedia.txt` | 416 MB |
| `data/shakespeare_char/input.txt` | 1.1 MB |
| `data/fineweb/train_fineweb.txt` | 0 B (empty stub) |

## `/mnt/data/nanochat`

**No training text files at all.** I checked:
- The repo contains only code + `.venv` (7.7 GB of Python packages, not data)
- No `.bin`, `.npy`, `.parquet`, or large `.txt` training files anywhere
- Its pretraining data (`ClimbMix-400B` parquet shards) is downloaded **on demand from HuggingFace** (`NANOCHAT_DATA_DIR` / `~/.cache/nanochat/base_data_climbmix`) and currently isn't stored locally — `~/.cache/nanochat` only has tokenizer/eval files, no dataset shards.

**Answer:** the largest training text file is `train_fineweb.old.txt` at **16 GB**, located in `/mnt/data/nanoGPT` (here).

Note: if you're asking about raw non-text data, nanoGPT's `data/fineweb/edu_fineweb100B/` holds **285 GB** of `.npy` token shards, which dwarfs everything else.