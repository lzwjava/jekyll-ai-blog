---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Completed and Inference Commands
translated: false
type: note
---

Training stopped cleanly at iter ~15180 (last checkpoint = step 15000, val loss **3.0259**, train loss **3.0510**).

## Inference command

Run this in tmux 7 (or any shell), from `/mnt/data/nanoGPT`:

```bash
source venv/bin/activate
python sample.py \
  --out_dir=out-fineweb-gpt3 \
  --start="Once upon a time" \
  --num_samples=3 \
  --max_new_tokens=200 \
  --temperature=0.8 \
  --top_k=200 \
  --device=cuda \
  --dtype=bfloat16
```

Useful variants:

```bash
# Interactive: read prompt from a file
python sample.py --out_dir=out-fineweb-gpt3 --start=FILE:prompt.txt

# Read prompt from stdin
python sample.py --out_dir=out-fineweb-gpt3 --start="$(cat)"

# More deterministic
python sample.py --out_dir=out-fineweb-gpt3 --temperature=0.6 --top_k=40 --start="The president said"

# More creative
python sample.py --out_dir=out-fineweb-gpt3 --temperature=1.0 --top_k=500
```

Heads up — val loss 3.03 is roughly on par with the GPT-2 124M baseline (~3.11), so output should be locally coherent but won't be GPT-3 quality despite the dir name. If you want to keep training later, just re-run your original train command; nanoGPT will resume from `ckpt.pt` if `init_from='resume'` is set in your config.
