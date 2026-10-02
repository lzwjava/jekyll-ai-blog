---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载和运行Gemma模型
translated: true
type: note
---

是的！**llama.cpp 完全支持 Gemma 模型**（Gemma 1、Gemma 2 以及更新的 Gemma 3）。我在你的模型文件夹中看到了 `ggml-vocab-gemma-4.gguf`，确认已内置支持。

不过你还没有下载 Gemma 模型。要运行一个模型，可以：

**选项 1：从 Hugging Face 下载 GGUF 文件**

例如，Gemma 2 9B（指令版）：
```bash
cd ~/projects/llama.cpp
wget -O models/gemma-2-9b-it-Q4_K_M.gguf \
  https://huggingface.co/bartowski/gemma-2-9b-it-GGUF/resolve/main/gemma-2-9b-it-Q4_K_M.gguf
```

**选项 2：从原始 Gemma 转换（如果你有的话）**

如果你已经有来自 Kaggle/Google 的原始 Gemma 模型：
```bash
python convert_hf_to_gguf.py --outfile models/gemma-2-9b.gguf /path/to/gemma-model/
./build/bin/llama-quantize models/gemma-2-9b.gguf models/gemma-2-9b-Q4_K_M.gguf Q4_K_M
```

**然后用 llama-server 运行：**
```bash
./build/bin/llama-server -m models/gemma-2-9b-it-Q4_K_M.gguf --port 8080
```

**更小的选择**——Gemma 2 2B 占用更少的 VRAM（Q4 量化下约 2GB）：
```bash
wget -O models/gemma-2-2b-it-Q4_K_M.gguf \
  https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf
```

你的 GPU 有约 24GB VRAM（从显示的 2099MiB 使用量来看），因此 Gemma 2 9B 在 Q4 量化下（约 6-7GB）可以流畅运行。需要我帮你下载并启动一个吗？