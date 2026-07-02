---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing VRAM OOM on Large Batches
translated: false
type: note
---

VRAM is hitting the wall at batch_size=16. The loss computation expands logits to `[batch*seq_len, vocab_size]` which spikes memory. Two fixes:

1. **Reduce batch size** to 8 (effective batch stays 16 with grad_accum=2)
2. **Set the env var** the error suggests

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate && PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True python3 train_whisper.py --model small --batch-size 8 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000
```

If that still OOMs, drop to `--batch-size 4 --grad-accum 4` (same effective batch 16).
