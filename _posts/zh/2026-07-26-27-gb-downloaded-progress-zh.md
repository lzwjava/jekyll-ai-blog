---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 27 GB 下载进度
translated: true
type: note
---

下载进展顺利！**已完成 27 GB** ✅

以下是已下载的内容：

| 文件 | 大小 | 状态 |
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

### 📋 如何监控

```bash
# 查看实时进度
ssh -p 31005 root@36.150.116.206 "tmux attach -t flux-download"

# 检查大小增长
ssh -p 31005 root@36.150.116.206 "du -sh /root/FLUX.1-schnell/"

# 列出文件
ssh -p 31005 root@36.150.116.206 "ls -lh /root/FLUX.1-schnell/*.safetensors"
```

下载正在后台通过 `tmux` 运行，即使断开连接也会继续。