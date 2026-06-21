---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Dataset Analysis and Verdict
translated: false
type: note
---

Now I have a complete picture. Here's the analysis:

================================================================
CODE DATASETS EXPLORATION — ANALYSIS
================================================================

## 1. The Stack v2 (bigcode/the-stack-v2-dedup)

| Item | Details |
|------|---------|
| Size | 67.5TB full / 32.1TB dedup |
| Tokens | ~900B |
| Languages | 658 |
| Format | SWHIDs only (file IDs, NOT actual code) |

VERDICT: **NOT practical.** The HF dataset only stores Software Heritage IDs, not code content. To get actual files you need:

- AWS S3 credentials for softwareheritage bucket
- Agreement with Software Heritage + INRIA
- Download file-by-file via S3 API

This is designed for BigCode's internal pipeline, not for individual download.

## 2. The Stack v1 (bigcode/the-stack)

| Item | Details |
|------|---------|
| Size | 6.4TB full / 2.9TB dedup |
| Tokens | ~200B |
| Languages | 358 |
| Format | Direct code content |

VERDICT: **Possible but requires agreement.** You must accept terms on HF, share contact info. At 2.9TB dedup it barely fits on this 1.8TB disk. Would need selective language download.

## 3. codeparrot/github-code

| Item | Details |
|------|---------|
| Size | ~1TB uncompressed / ~300GB compressed |
| Tokens | 115M files |
| Languages | 32 |
| Format | Direct code, streamable from HF |

VERDICT: **BEST OPTION for this machine.** Directly downloadable, no special agreement. 1TB fits on disk (972GB free). Has Python, JS, TS, C++, Rust, Go, Java, etc. Streamable via `datasets` library.

## 4. bigcode/the-stack-smol

| Item | Details |
|------|---------|
| Size | 2.6GB |
| Samples | 300K files |
| Languages | 30 |
| Format | Direct code content |

VERDICT: **Good for testing only.** Too small for real pretraining (~100M tokens). But useful to validate your pipeline before committing to a big download.

## 5. nampdn-ai/tiny-codes

| Item | Details |
|------|---------|
| Size | ~2GB |
| Samples | 1.6M snippets |
| Languages | 11 |
| Focus | Reasoning via code (if/else, logic) |

VERDICT: **Fine-tuning data, not pretraining.** Inspired by "Textbooks Are All You Need". Good to mix in at small比例 for reasoning boost, but too small and synthetic for pretraining.

## 6. FineWeb / FineWeb-Edu (already on disk)

| Item | Details |
|------|---------|
| On disk | 285GB (nanoGPT shards) + 374GB (zz-backup parquet) |
| Content | English web text (articles, blogs, forums) |
| Code content | Very little — this is NOT a code dataset |

VERDICT: **Already processed, but wrong data for code training.** FineWeb is general web text. It has some incidental code (StackOverflow answers, tutorials) but it's not a code corpus. Your existing 760M config uses this for general LM training.

## 7. StarCoder training repos

| Repo | Purpose |
|------|---------|
| bigcode-project/starcoder | Fine-tuning + inference scripts only |
| bigcode-project/starcoder2 | Fine-tuning with LoRA/PEFT |

VERDICT: **Not useful for pretraining.** These repos contain fine-tuning code, not the pretraining pipeline. StarCoder2 was pre-trained using a fork of Megatron-LM (not publicly released as a clean repo).

================================================================
RECOMMENDATION FOR YOUR SETUP
================================================================

Your machine: RTX 4070 (12GB), 64GB RAM, 972GB free disk.

**Step 1: Test with the-stack-smol (2.6GB)**

```bash
pip install datasets
python3 -c "
from datasets import load_dataset
ds = load_dataset('bigcode/the-stack-smol', split='train')
print(ds)
print(ds[0])
"
```

**Step 2: Download codeparrot/github-code (~300GB compressed)**
This is the best real code dataset that's directly downloadable. You can filter by language if disk is tight:

```bash
python3 -c "
from datasets import load_dataset
# Download just Python subset first
ds = load_dataset('codeparrot/github-code', streaming=True, split='train',
                  languages=['Python'])
# Process into nanoGPT format...
"
```

**Step 3: Mix with FineWeb-Edu**
For a code+general LM, mix 70% code + 30% FineWeb-Edu. Your existing nanoGPT data pipeline handles this.

================================================================

Want me to download the-stack-smol for a quick test, or start pulling codeparrot/github-code (Python subset first)?
