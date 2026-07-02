---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复大批量训练中VRAM内存溢出
translated: true
type: note
---

在 `batch_size=16` 时，VRAM 资源告急。损失计算会将 logits 扩展为 `[batch*seq_len, vocab_size]` 的尺寸，导致内存激增。两种解决方案：

1. **将批大小降至 8**（配合 `grad_accum=2` 保持有效批大小为 16）
2. **设置错误提示中建议的环境变量**

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate && PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True python3 train_whisper.py --model small --batch-size 8 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000
```

若仍出现显存溢出，可进一步降低至 `--batch-size 4 --grad-accum 4`（保持有效批大小仍为 16）。
