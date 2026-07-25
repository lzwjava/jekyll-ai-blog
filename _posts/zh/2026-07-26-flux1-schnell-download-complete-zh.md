---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.1-schnell 下载完成
translated: true
type: note
---

## ✅ 下载完成！🎉

**FLUX.1-schnell** 已完全下载！以下是最终状态：

| 文件 | 大小 | 状态 |
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
| **总计** | **54 GB** | ✅ **完成** |

tmux 会话已结束并退出。没有残留的不完整文件。现在你可以使用以下命令加载它：

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