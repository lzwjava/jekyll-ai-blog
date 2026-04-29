---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Memory Issue and Training Options
translated: false
type: note
---

Health check done. Summary:

**Good signs ✓**
- Config loads, data loads
- Model = **123.59M parameters** (confirmed GPT-2 124M arch)
- 524,288 tokens per iter (batch 8 × block 1024 × grad_accum 64)

**Problem ✗** — OOM on backward pass:
- GPU: RTX 4070, 12 GB total
- `llama-server` (PID 2202) is holding **5.9 GB**
- Only ~5.7 GB left → not enough for batch 8 × block 1024 fp16 backward

The original 11,500-iter checkpoint clearly trained when the GPU was free. To train again you have two options:

**Option A — free the GPU first (recommended, matches original training config):**
```bash
kill 2202    # stop llama-server
nvidia-smi   # confirm GPU is empty
python3 train.py config/train_fineweb.py
```

**Option B — keep llama-server, train with smaller per-step batch (same effective batch size via more grad-accum):**
```bash
python3 train.py config/train_fineweb.py --batch_size=2 --gradient_accumulation_steps=256 --compile=False
```

In both cases, watch for `iter 0: loss ~10.9` then dropping. Ctrl+C anytime — you can restore the trained checkpoint with:
```bash
mkdir -p out-fineweb && cp out-fineweb-backup/ckpt.pt out-fineweb/ckpt.pt
```