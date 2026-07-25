---
audio: false
generated: true
image: false
lang: en
layout: post
title: 27 GB Downloaded Progress
translated: false
type: note
---

Download is progressing well! **27 GB done so far** ✅

Here's what's been downloaded:

| File | Size | Status |
|------|------|--------|
| `ae.safetensors` | 320 MB | ✅ |
| `text_encoder/model.safetensors` | 235 MB | ✅ |
| `text_encoder_2/model-00001-of-00002` | 4.7 GB | ✅ |
| `text_encoder_2/model-00002-of-00002` | 4.3 GB | ✅ |
| `transformer/...-00003-of-00003` | 3.7 GB | ✅ |
| `vae/diffusion_pytorch_model.safetensors` | 160 MB | ✅ |
| `transformer/...-00001-of-00003` | ~3.7 GB | 🔄 |
| `transformer/...-00002-of-00003` | ~3.7 GB | ⏳ |
| `flux1-schnell.safetensors` | ~30+ GB | ⏳ |

### 📋 How to monitor

```bash
# See real-time progress
ssh -p 31005 root@36.150.116.206 "tmux attach -t flux-download"

# Check size growing
ssh -p 31005 root@36.150.116.206 "du -sh /root/FLUX.1-schnell/"

# List files
ssh -p 31005 root@36.150.116.206 "ls -lh /root/FLUX.1-schnell/*.safetensors"
```

The download is running in the background via `tmux` and will keep going even if you disconnect.
