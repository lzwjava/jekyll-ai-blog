---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX Model Size Comparison
translated: false
type: note
---

Here's the comparison:

## 🔄 FLUX.2-dev vs FLUX.1-dev

| Feature | FLUX.2-dev | FLUX.1-dev |
|---------|-----------|-----------|
| **Total size** | **~177 GB** | **~69 GB** |
| **Pipeline** | `image-to-image` | `text-to-image` |
| **Gated** | ✅ auto | ✅ auto |
| **Downloads** | 1.3M | 569K |
| **Likes** | 1,941 | 13,786 |

FLUX.1-dev is **much smaller** (69 GB vs 177 GB) because it uses:
- Single-file T5 text encoder (vs 10 shards in 2-dev)
- CLIP text_encoder_2 (2 shards)
- Transformer in 3 shards (vs 7 shards)
- Simpler VAE (no separate `ae.safetensors`)

**However**, both are **gated** — you still need to:
1. Accept the license at https://huggingface.co/black-forest-labs/FLUX.1-dev
2. Provide a HuggingFace **read token**

If you've already accepted the license for FLUX.1-dev, I can start the download right away. Which one do you want to go with?
