---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX模型下载进度更新
translated: true
type: note
---

以下是当前状态：

**已完成的工作：**
1. 在 /home/lzw/projects/flux2/.venv 目录下创建了 Python 3.12 虚拟环境
2. 安装了所有依赖（torch 2.8+cu129、transformers、safetensors 等）
3. 检测到你的 GPU：RTX 4070（12GB 显存）—— 完美适配 FLUX.2 [klein] 4B 模型
4. 首次从 huggingface.co 下载时速度约为 54 KB/s
5. 切换到 hf-mirror.com（HF_ENDPOINT=https://hf-mirror.com）后速度达到约 30 MB/s
6. 较小的 safetensors 文件（778MB）已下载完成
7. 较大的 safetensors 文件（4.41GB）在达到迭代限制时已下载约 74%

**当前状态：**
后台下载进程（proc_567395c17054）可能仍在运行，正在下载 4.41GB 模型文件中剩余的约 1.1GB。之后还需要下载文本编码器（Mistral-Small-3.2-24B-Instruct-2506）和自编码器（ae.safetensors），这些是额外的下载项。

**要完成我未完成的工作，请自行运行以下命令：**
```bash
cd /home/lzw/projects/flux2
HF_ENDPOINT=https://hf-mirror.com .venv/bin/python scripts/cli.py
```
然后在提示时选择选项 1（flux.2-klein-4b）。部分下载的模型文件将从缓存中继续下载。所有权重下载完成后，你将获得一个交互式提示，可以输入任何文本提示词来生成图像。

**关键提示：** `HF_ENDPOINT=https://hf-mirror.com` 标志至关重要 —— 如果没有它，从 huggingface.co 下载在你的网络环境下几乎无法使用（约 50 KB/s）。使用镜像后，速度可达约 30 MB/s。