---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Dataset Variations and Tokenization
translated: false
type: note
---

You're right — they're NOT duplicates. Here's what each is:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /root/zz/datasets/fineweb-edu/     (40 GB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  14 parquet files (2.2-2.3 GB each)
  Raw text from HuggingFace FineWeb-Edu
  Human-readable, can be reprocessed
  Source: https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /root/nanoGPT/data/fineweb/edu_fineweb100B/  (28 GB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  147 .npy files (191 MB each)
  Tokenized with GPT-2 BPE tokenizer
  Machine-readable numpy arrays of token IDs
  Ready for training — this is what train.py reads

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Why tokenized is smaller:
- Tokenization compresses text (common words → single token IDs)
- No metadata overhead (just uint16 arrays)
- Parquet has row groups, column metadata, compression dictionaries

They're complementary, not duplicate:
- **Parquet** = source of truth, human-readable, reprocessable
- **NPY** = training-ready, fast random access for DataLoader

**Can you delete the parquet?** Yes, if you:
- Don't plan to re-tokenize with a different tokenizer
- Don't need to change preprocessing (chunk size, filtering)
- Have the NPY files already (you do — 147 files, 28GB)

```bash
# Free 40 GB — safe if you won't re-tokenize
rm -rf /root/zz/datasets/fineweb-edu
```

But if you later want to switch to nanochat (which uses its own tokenizer/preprocessing), you'd need to re-download the parquet. Your call.