---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Llama.cpp与旧GPU的向后兼容性
translated: true
type: note
---

简短回答：因为 llama.cpp 的 CUDA build 特意保持与旧版 NVIDIA GPU（如 M40）的 backward-compatible，并在运行时根据 GPU 的 compute capability 调整其 kernels。

M40 是 **Maxwell** (GM200)，compute capability **5.2**，12/24 GB GDDR5。有三个因素使其能够工作：

**1. 二进制文件包含 PTX，而不仅仅是 SASS**
在 `ggml/src/ggml-cuda/CMakeLists.txt` 中，默认构建包含 `50-virtual`（只要 CUDA toolkit 版本低于 13）：

```cmake
if (CUDAToolkit_VERSION VERSION_LESS "13")
    list(APPEND CMAKE_CUDA_ARCHITECTURES 50-virtual 61-virtual 70-virtual)
endif ()
```

`-virtual` 意味着 kernels 被编译成 PTX，**CUDA driver JIT-compiles** 在首次启动时将它们编译为适用于你确切 GPU 的 native code。这就是为什么同一个 build 既能在 M40 上运行，也能在现代 RTX 卡上运行。

**2. CUDA backend 根据 GPU 的 compute capability 在运行时切换 kernels**

- CUDA graphs 在低于 Volta 的 GPU 上被禁用（`ggml-cuda.cu:4833`）。
- Flash attention 会回退到不需要 tensor cores 的路径（CC < 70）。
- Quantized matmuls 为 pre-Volta GPU 选择更慢但兼容的 kernels（`mmvq.cu:1163`，例如 `Q2_K`/`Q3_K`/`IQ3_S` 在 Pascal 及更老的 GPU 上使用 fallback）。
- FP16 math 在 Maxwell 慢的地方降级为 FP32。

**3. Maxwell 是 supported hardware range 的底线——代码库将 CC 5.0 视为最低支持的 NVIDIA arch。**

**注意：** 它 *能工作*，但速度不快。M40 没有 tensor cores，没有 fast FP16，也没有 `__dp4a` (sm_61+)，所以 quantized inference 比现代卡慢很多。另外要注意：**CUDA 13 放弃了对 Maxwell 的支持**，所以如果你的 build 在 M40 上加载失败，你需要 CUDA 12.x toolkit（或更旧版本）。

如果你指的是更具体的问题（特定的模型、崩溃或关于 M40 的性能问题），请确切告诉我你观察到了什么，我会进一步探究。
