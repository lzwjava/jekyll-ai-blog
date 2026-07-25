---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX.1-schnell Download Complete
translated: false
type: note
---

## ✅ Download Complete! 🎉

**FLUX.1-schnell** is fully downloaded! Here's the final state:

| File | Size | Status |
|------|------|--------|
| `flux1-schnell.safetensors` | **23 GB** | ✅ |
| `transformer/...00001` | 9.3 GB | ✅ |
| `transformer/...00002` | 9.3 GB | ✅ |
| `transformer/...00003` | 3.7 GB | ✅ |
| `text_encoder_2/...00001` | 4.7 GB | ✅ |
| `text_encoder_2/...00002` | 4.3 GB | ✅ |
| `text_encoder/model.safetensors` | 235 MB | ✅ |
| `ae.safetensors` | 320 MB | ✅ |
| `vae/...safetensors` | 160 MB | ✅ |
| **Total** | **54 GB** | ✅ **Done** |

The tmux session has finished and exited. No incomplete files remain. You can now load it with:

```bash
source /opt/venv/bin/activate
python -c "
from diffusers import FluxPipeline
import torch
pipe = FluxPipeline.from_pretrained('/root/FLUX.1-schnell', torch_dtype=torch.bfloat16)
pipe.to('cuda')
# ... generate!
"
```
