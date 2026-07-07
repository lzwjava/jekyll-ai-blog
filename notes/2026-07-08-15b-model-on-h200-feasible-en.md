---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1.5B Model on H200 Feasible
translated: false
type: note
---

## 1.5B Model on H200 — Feasibility Analysis

**Yes, it's feasible.** Based on the codebase analysis:

### Reference (MI300X): `760M` at batch=32 → 105 GB / 192 GB

### H200 advantage:
- **FA3** (Flash Attention 3) — much lower activation memory than SDPA on AMD
- **FP8** support — can halve memory on matmuls
- Higher MFU (~45% vs 27%)

### Suggested Config for ~1.5B

| Param | Value | Notes |
|-------|-------|-------|
| `--depth` | **30** | base_dim=1920, model_dim=1920 (clean 15×128 heads) |
| `--aspect-ratio` | 64 | standard |
| `--head-dim` | 128 | FA3 sweet spot |
| `--device-batch-size` | **16** | half of MI300X to fit 140 GB vs 192 GB |
| `--total-batch-size` | 524288 | same as reference |
| `--max-seq-len` | 2048 | standard |
| `--window-pattern` | SSSL | alternating sliding window |
| `--fp8` | optional | saves ~40% VRAM, H200 supports it |

**Params:** ~1.45B (30 layers × 1920 dim × 15 heads)
**Chinchilla-optimal data:** ~29B tokens (20× params) — fits in our 35.8B token dataset
**Steps:** ~55,000 at 524K tokens/step
**Est. VRAM:** ~110-120 GB (with FA3, batch=16) — fits in 140 GB
**With FP8:** ~80-90 GB — comfortable fit

### Command

```bash
cd /workspace/zz
tmux new -s train-1.5b
python -m scripts.base_train \
  --depth=30 \
  --device-batch-size=16 \
  --total-batch-size=524288 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --target-param-data-ratio=20 \
  --eval-every=500 \
  --save-every=5000 \
  --run=h200-d30-1.5b \
  --tracker=wandb
```

Want me to run it?
