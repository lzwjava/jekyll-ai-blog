---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attn单架构编译
translated: true
type: note
---

状态更新：

- **1个nvcc进程** — flash-attn 始终按顺序编译 `.cu` 文件，不受 MAX_JOBS/ninja 影响
- **已完成2个.o文件**，当前正在编译 `flash_bwd_hdim128_bf16_sm80.cu`
- **9个tmpxft临时文件** — 仍在早期阶段（反向传播，hdim 128）
- **架构：仅sm_89** — 这才是真正的加速（每个文件比4架构编译快约4倍）

MAX_JOBS=32 在这里帮不上忙 — flash-attn 的构建系统一次只编译一个 `.cu` 文件。瓶颈在于单个文件的 CUDA 编译。使用单架构时，每个文件应只需1-3分钟，而不是5-12分钟。估计剩余总共约30-40分钟。