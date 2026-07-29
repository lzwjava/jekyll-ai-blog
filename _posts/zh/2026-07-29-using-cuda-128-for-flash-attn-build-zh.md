---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用CUDA 12.8构建Flash-Attn
translated: true
type: note
---

CUDA 12.8 位于 `/usr/local/cuda-12.8/bin/nvcc`。默认的 `nvcc` 是 CUDA 13.2（因此构建过程选择了 13.2）。你需要显式使用 CUDA 12.8。

## 正确的安装命令

```bash
CUDA_HOME=/usr/local/cuda-12.8 \
PATH=/usr/local/cuda-12.8/bin:$PATH \
MAX_JOBS=16 \
TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

这将：
1. ✅ 使用 **CUDA 12.8**（与 PyTorch 2.10.0+cu128 匹配）
2. ✅ 仅构建 **sm_89** 内核（RTX 4070）——编译速度提升约 10 倍
3. ✅ 运行 **16 个并行任务**（之前为 2 个）
4. ✅ 运行时无 ABI 不匹配问题

预期编译时间：**约 3–8 分钟**，而非之前的 20–60 分钟以上。