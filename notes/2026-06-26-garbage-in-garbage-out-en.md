---
audio: false
generated: true
image: false
lang: en
layout: post
title: Garbage in, garbage out
translated: false
type: note
---

There it is — total garbage across the board. Spaces, HTML fragments, random symbols.

Here's the command if you want to run it yourself and play with prompts/temperature:

```
cd /mnt/data/nanoGPT && python3 sample.py \
  --out_dir=out-github-code-124m \
  --num_samples=3 \
  --max_new_tokens=300 \
  --temperature=0.8 \
  --top_k=40 \
  --start="def quicksort(arr):
"
```

Change `--start=` to try different prompts. But the output will be bad regardless — the model learned to output spaces and HTML fragments because 46% of the training data was noise (HTML docs, license headers, config stubs). Only 54% was actual code.

The fix is cleaning the data and retraining. Want me to write a filter script?
