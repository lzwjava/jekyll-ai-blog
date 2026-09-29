---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb-Edu 100B Largest Dataset
translated: false
type: note
---

Here's the full dataset comparison across both projects:

## Datasets in `/mnt/data/nanoGPT` (here)

| Dataset | Location | Size | Format |
|---|---|---|---|
| **FineWeb-Edu 100B** | `data/fineweb/edu_fineweb100B/` | **263 GB** | 1408 × 191 MB `.npy` shards ⬅ largest |
| FineWeb text | `data/fineweb/train_fineweb.old.txt` | 16 GB | raw text |
| FineWeb tokens | `data/fineweb/train.bin` | 6.9 GB | tokenized uint16 |
| Wikipedia | `data/wikipedia_local/` | 580 MB | text + bins |
| Shakespeare | `data/shakespeare_char/` | 3.3 MB | text |
| sec-edgar | `data/sec-edgar/` | 0 B | empty (data lives in `/mnt/data/sec-edgar-gpt*`) |

## Datasets in `/mnt/data/nanochat`

**None stored locally.** Its pretraining corpus (ClimbMix-400B, ~400B tokens) is downloaded on demand from HuggingFace in 191 MB parquet shards (`~/.cache/nanochat/base_data_climbmix/`), which currently doesn't exist on disk. Only tokenizer/eval assets (~30 MB) are cached.

## Related datasets elsewhere in `/mnt/data`

| Dataset | Size |
|---|---|
| `bilingual-gpt/` (used by `out-bilingual`) | 25 GB — `mixed.txt` 11 GB text, plus 7.5 GB + 3.3 GB jsonl shards |
| `sec-edgar-gpt/` | 985 MB |
| `sec-edgar-gpt-124m/` | 955 MB |
| `cache/` | 77 GB (likely HF/tokenizer cache) |
| `bigcode-dataset/` | 20 MB |

## Bottom line

The **largest dataset is the FineWeb-Edu 100B token shards at 263 GB** in `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B/`. nanochat has no local training dataset at all (it streams from HuggingFace). If you count raw text only, the 16 GB `train_fineweb.old.txt` here is still the winner.