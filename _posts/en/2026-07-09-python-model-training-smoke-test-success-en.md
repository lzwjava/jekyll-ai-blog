---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Model Training Smoke Test Success
translated: false
type: note
---

Smoke train completed successfully. Run on RTX 4070:

| Component | Time | Result |
|-----------|------|--------|
| Tokenizer (4k vocab) | 3.6s | Trained on 50M Python chars |
| Pretrain (depth=4, 20 steps) | ~1s | Loss 8.32→8.19, 310k tok/s, 30% MFU |
| Peak memory | 151 MB | Barely touched 12 GB |

The samples already show Python-ish output (`class`, `return`, `import`, license headers) — data pipeline works end-to-end.

For real training:
```bash
bash /mnt/data/zz/codeparrot/train_codeparrot.sh
```
(~28 hours for depth=12, 87k steps, 286M params, 24.7B tokens)