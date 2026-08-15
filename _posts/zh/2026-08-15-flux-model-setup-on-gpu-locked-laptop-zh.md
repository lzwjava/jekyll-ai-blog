---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在GPU锁定笔记本电脑上设置Flux模型
translated: true
type: note
---

已找到所有内容。以下是完整情况：

## FLUX.1-schnell 在本笔记本电脑上的位置

**1. 官方 HuggingFace 缓存**（完整 diffusers 格式，2.3 GB）：
```
/home/lzw/.cache/huggingface/hub/models--black-forest-labs--FLUX.1-schnell
```

**2. 你实际运行的工作配置**（stable-diffusion.cpp 配合量化 GGUF）：
```
二进制文件：/mnt/data/zz/flux/sd_cpp/build/bin/sd-cli
模型：/mnt/data/zz/flux/models/
  ├── flux1-schnell-Q4_0.gguf      (6.3G — 模型)
  ├── ae.safetensors               (320M — VAE)
  ├── clip_l.safetensors           (235M — 文本编码器)
  └── t5xxl_fp16.safetensors       (9.2G — 文本编码器)
```

加上你自己的 CLI 包装器 `fluxreel`（安装在 `~/.local/bin/fluxreel`），它封装了 sd-cli 配置。

## 如何运行

```bash
# 最简单的方式 — 你的包装器
fluxreel img "a cat astronaut riding a rocket"

# 或直接通过 sd-cli
/mnt/data/zz/flux/sd_cpp/build/bin/sd-cli \
  --model /mnt/data/zz/flux/models/flux1-schnell-Q4_0.gguf \
  --vae /mnt/data/zz/flux/models/ae.safetensors \
  --clip_l /mnt/data/zz/flux/models/clip_l.safetensors \
  --t5xxl /mnt/data/zz/flux/models/t5xxl_fp16.safetensors \
  --cfg-scale 1.0 --steps 4 --width 768 --height 768 \
  --output flux_out.png --prompt "a cat astronaut riding a rocket"
```

## ⚠️ 当前阻塞因素

**你的 RTX 4070（12 GB）** 被一个训练任务完全占用：

```
PID 522494  python3.12 train.py config/train_bilingual.py   (已运行 22 小时 53 分钟)
cwd: /mnt/data/nanoGPT
GPU：已使用 8.7 GB VRAM，GPU 利用率 100%  →  仅剩约 1.7 GB 空闲
```

`fluxreel img` 需要约 10 GB VRAM 预算（4 GB 模型 + 文本编码器），因此在该训练任务运行时会出现 OOM 或失败。

**你的选项：**
1. 等待 nanoGPT 训练完成（仅剩约 1.7 GB 空闲，不够用），或
2. 停止训练任务后再运行 flux。

需要我终止 nanoGPT 训练进程（PID 522494）以便你生成图像吗？它已经运行了约 23 小时，你可能想先检查 `/mnt/data/nanoGPT` 中的检查点进度。