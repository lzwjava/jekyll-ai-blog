---
audio: false
generated: true
image: false
lang: en
layout: post
title: Interrupted model upload resume
translated: false
type: note
---

Here's the status:

**Analysis (done)**

- Model: GPT-2 124M (12 layers, 768 hidden, 12 heads, 1024 ctx, vocab 50257)
- Files: config.json, generation_config.json, tokenizer.json, tokenizer_config.json, model.safetensors (622MB float32)
- Missing: README.md (model card) — fixed, uploaded to server

**Upload progress**

- Repo created: <https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf> ✓
- hf CLI installed on server (47.86.12.246) ✓
- HF token configured ✓
- README.md (model card) created + copied to server ✓
- Upload started — got 133MB/622MB into model.safetensors before interrupted (signal 15, likely SSH timeout)

**What's left**

- Resume the upload. The small files (5/6) already transferred, only model.safetensors remains (~489MB left)

Want me to resume the upload? I'll run it in background so it doesn't timeout:

```bash
ssh root@47.86.12.246 "nohup hf upload lzwjava/sec-edgar-gpt-124m-hf ~/sec-edgar-gpt-124m-hf/ > /tmp/hf-upload.log 2>&1 &"
```

Or I can start it now with a longer timeout. Which do you prefer?
