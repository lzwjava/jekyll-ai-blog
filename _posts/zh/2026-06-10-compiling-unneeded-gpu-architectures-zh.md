---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 编译不需要的GPU架构
translated: true
type: note
---

以下是完整情况：

**并行性：**

- nvcc `--threads 4` — 同时为4种架构编译
- 4个cicc进程，每个CPU占用约100%，内存约650MB
- 32个核心可用，平均负载2.90 — 有充足的余量

**问题 — 为所有架构编译：**
构建过程忽略了`TORCH_CUDA_ARCH_LIST="8.9"`。flash-attn的构建系统硬编码了4个目标：

```
-gencode arch=compute_80,code=sm_80   ← H100（对你来说是浪费）
-gencode arch=compute_90,code=sm_90   ← Ada（浪费）
-gencode arch=compute_100,code=sm_100 ← Blackwell（浪费）
-gencode arch=compute_120,code=sm_120 ←（浪费）
```

你的RTX 4070是sm_89，这些没有一个完全匹配。它正在编译大约所需4倍的内核。

**当前内核：** `flash_bwd_hdim32_fp16_causal_sm80` — 仍然在反向传播的早期阶段。

**资源：** 良好 — 53GB可用内存，34GB可用磁盘。

需要我终止这个进程，并用`MAX_JOBS=8 FLASH_ATTN_CUDA_ARCHS="8.9"`环境变量（flash-attn的setup确实会遵守这个变量）重新启动，以将速度提升4倍吗？还是让它继续运行？
