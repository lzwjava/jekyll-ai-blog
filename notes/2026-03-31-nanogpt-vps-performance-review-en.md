---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanoGPT Performance Review on Cheap VPS
translated: false
type: note
---

Here's the full review, Boss:

---

## 🦞 nanoGPT on VPS — Comprehensive Review

### Server Specs
- **CPU**: DO-Regular (DigitalOcean droplet), 1 vCPU
- **RAM**: 458 MB (was OOM without swap — added 1GB swap file)
- **Disk**: 8.7 GB total, 4.0 GB free after install

### Model
- **Architecture**: 6-layer, 6-head, 384-embedding GPT (character-level)
- **Parameters**: 10.65M
- **Vocab**: 65 characters (Shakespeare character set)
- **Context window**: 256 tokens
- **Checkpoint**: ~124 MB

### Training Status
- **Dataset**: Shakespeare character-level (1.06 MB raw text)
- **Trained**: 2,000 / 5,000 iterations (40% done)
- **Best val loss**: 1.4716 (decent but could improve with more training)
- **Config**: batch 64, lr 0.001, dropout 0.2, weight decay 0.1

### Inference Performance (CPU)

| Tokens | Time | Speed |
|--------|------|-------|
| 50 | 1.28s | 39.1 tok/s |
| 100 | 3.56s | 28.1 tok/s |
| 200 | 11.27s | 17.7 tok/s |

Speed drops with longer sequences (KV cache grows, memory-bound on this tiny box).

### Memory Usage
- **Model load**: 310 MB RSS (needs swap on 458MB machine)
- **Swap used**: 89 MB during inference — manageable but not ideal

### Output Quality
The generated text is recognizably Shakespearean — proper character names (CORIOLANUS, VOLUMNIA, JULIET), period-appropriate phrasing. But at 40% training and only 10M params, it drifts into incoherence after ~30-40 characters. More training would help.

### Verdict
It works, but this VPS is underpowered for anything serious. Fine for a demo or learning. If you want better output, either:
1. **Train more** (finish the remaining 3,000 iters — probably 1-2 hours on CPU)
2. **Use a beefier box** — even 2GB RAM would eliminate the swap dependency