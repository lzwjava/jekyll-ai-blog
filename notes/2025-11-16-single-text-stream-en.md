---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Train on a Single Concatenated Text Stream
translated: false
type: note
---

In nanoGPT (and essentially in any GPT-style training, including the original GPT-2/GPT-3 training), **you must train on one single gigantic concatenated text stream**, not on individual articles/documents fed one-by-one as separate sequences.

Here’s why and exactly how it’s done in practice with FineWeb (and in Andrej’s nanoGPT code):

### What you should do (correct way)
1. Concatenate **all** the individual articles into **one huge .txt file** (or multiple large shard files), separated only by a special end-of-text token `<|endoftext|>` (or whatever separator you choose).
2. During training, nanoGPT will:
   - Load the entire concatenated text into one giant token array.
   - Split it into fixed-length blocks (e.g., block_size = 1024 tokens).
   - These blocks very frequently cross document boundaries — that’s not only okay, it’s desirable.

This is exactly how OpenAI trained GPT-2 and GPT-3, and it’s what Andrej does with Shakespeare, OpenWebText, FineWeb-Edu, etc.

### What the extract_fineweb.py script is doing
That script you ran is already doing the right thing:

```bash
$ python ./scripts/train/extract_fineweb.py
```

It reads all the parquet files, extracts only the `text` column of every row (i.e., every webpage/article), writes the raw text one after another into `fineweb_extracted.txt`, and (in the latest versions) automatically inserts the `<|endoftext|>` separator between documents.

So the resulting file looks like:

```
<article 1 text> <|endoftext|> <article 2 text> <|endoftext|> <article 3 text> <|endoftext|> ...
```

That’s perfect. You should train on that single giant file (or the sharded bin files that `train.py` will create from it).

### What you should NOT do
- Do **not** feed each article as a separate example/sequence to the model and restart attention for every article.
- Do **not** truncate or pad every article to exactly block_size and train only within-document.
- Do **not** use Document-level batching where each sequence in the batch is one full document.

That would destroy the model’s ability to learn long-range dependencies that span multiple documents and would drastically hurt performance.

### Summary
Yes → Train on **one single massive concatenated text file** (exactly what `extract_fineweb.py` produces).
No → Do **not** train article-by-article as separate sequences.

That’s how GPTs have always been trained, and it’s the reason nanoGPT’s `train.py` just treats the data as one long token stream.

So just continue with the normal nanoGPT workflow:

```bash
python scripts/train/extract_fineweb.py   # you already did this
python train.py --dataset=your_extracted_file_or_fineweb10B etc.
```

You’re good to go!
