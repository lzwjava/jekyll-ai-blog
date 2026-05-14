---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running nanoGPT with pretrained GPT-2 models
translated: false
type: note
---

You need `transformers` first. One-liner:

```bash
cd /mnt/data/nanoGPT
source venv/bin/activate
pip install transformers
python sample.py --init_from=gpt2-medium --start="Hello, my name is" --num_samples=3 --max_new_tokens=200
```

That's it. `sample.py:47-49` routes `--init_from=gpt2*` into `GPT.from_pretrained`, which internally calls `transformers.GPT2LMHeadModel.from_pretrained('gpt2-medium')` (`model.py:260`). The first run downloads ~1.4 GB of weights to `~/.cache/huggingface/` and reuses them after.

Other valid values: `gpt2` (124M), `gpt2-medium` (350M), `gpt2-large` (774M), `gpt2-xl` (1558M).

Useful flags:
- `--device=cuda` (default) or `--device=cpu`
- `--temperature=0.8 --top_k=200` (sampling)
- `--start="FILE:prompt.txt"` to read prompt from a file