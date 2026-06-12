---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual SFT with Unsloth
translated: false
type: note
---

Done. Here's what's in `/mnt/data/zz/finetune/`:

```
finetune/
├── README.md              # full usage guide
├── requirements.txt       # pip deps
├── build_dataset.py       # extract en+zh posts → JSONL
├── train.py               # QLoRA SFT with Unsloth
├── eval.py                # compare fine-tuned vs base
├── export_gguf.py         # GGUF export for ollama
├── notes_sft.jsonl        # 21,434 examples (86MB)
├── notes_sft_train.jsonl  # 21,234 train (85MB)
└── notes_sft_eval.jsonl   # 200 eval (820KB)
```

Dataset stats:
- 10,726 English + 10,708 Chinese = 21,434 total
- 25.1M tokens, avg 1,169 tokens/example
- 30 posts skipped (too short < 100 chars)
- 200 held out for eval, rest for training

To train on the 4070:

```bash
cd /mnt/data/zz/finetune
pip install unsloth          # or: pip install -r requirements.txt
python train.py              # Qwen3-8B QLoRA 4-bit, ~2-4hrs
python train.py --model unsloth/Qwen3-4B   # smaller, faster
```
