---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070带来33倍加速
translated: true
type: note
---

### 🚀 前后对比 (RTX 4070)

| 阶段 | CPU (之前) | GPU (现在) | 加速比 |
| ------- | :-----------: | :--------: | :-------: |
| Text encoding | 2.2s | **0.3s** | 7× |
| Flux diffusion (4 steps) | ~487s | **12.8s** | 38× |
| VAE decode | 37s | **2.7s** | 13× |
| **总计** | **526s** | **~16s** | **33×** |

### 完成的操作

1. **使用 CUDA 重建了 `sd_cpp`** — `cmake -DSD_CUDA=ON` 检测到你的 RTX 4070（compute 8.9）
2. **停止了 `llama-server`** 以释放约 6 GB VRAM
3. **`run.sh` 中的关键优化**：
   - `--backend diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu` — Flux 和 VAE 在 GPU 上运行，文本编码器在 CPU 上运行
   - `--vae-tiling` — VAE 计算缓冲区从 **6.6 GB 降至 416 MB**，同时速度损失极小
   - `--max-vram 10` — 为桌面应用留出空间

### 发现的问题

- **T5XXL 文件** `t5xxl_fp16.safetensors` 存在损坏的张量（"data offsets out of bounds"）。没有此文件，提示遵循度会下降。请从[此处](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp16.safetensors)重新下载以修复。

### 使用方法

```bash
cd /mnt/data/zz/flux
./run.sh "your prompt here"
```

输出保存至 `outputs/flux_<timestamp>.png`（约 1.7 MB）。
