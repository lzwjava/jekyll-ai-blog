---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attn反向编译进展
translated: true
type: note
---

良好进展：

- 编译：`flash_bwd_hdim192_bf16`（反向，头维度192，bf16）
- 扩展：`flash_attn_2_cuda`
- 目前已生成56个临时文件
- 磁盘：34GB可用（稳定）
- 3个活跃编译进程

现在正在处理反向传递内核。仍有一段路要走——flash-attn有大约100多个内核变体（前向/反向 × fp16/bf16 × 头维度 64/96/128/192/256）。预计在约20-40分钟内完成。