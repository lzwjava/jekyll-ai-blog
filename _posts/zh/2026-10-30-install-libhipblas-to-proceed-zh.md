---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装libhipblas以继续
translated: true
type: note
---

模型正在下载（约4.36 GB，预计剩余约10分钟）。

现在构建阻塞点：llama.cpp的HIP后端需要libhipblas-dev，但它没有安装，而且这里的sudo需要密码。我无法输入。

请自行运行以下命令：

```bash
  sudo apt-get install -y libhipblas-dev
```

…或者粘贴你的sudo密码，我会继续（install → build with -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx900 → run inference）。

其他一切都已就绪：
- ✅ ~/projects/llama.cpp cloned (eb4e244)
- ✅ cmake 4.4.4 via uv installed
- ✅ ROCm/HIP 7.1 detected at /usr, GPU gfx900 (WX 9100, 16 GB VRAM)
- ⏳ Model downloading → ~/projects/llama.cpp/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf

一旦你解除对该包的限制，我将完成构建并运行一个测试推理。