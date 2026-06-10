---
audio: false
generated: true
image: false
lang: zh
layout: post
title: O文件的前进进度
translated: true
type: note
---

看起来不错：

- **编译了26个.o文件**（之前是15个）
- **当前：** `flash_fwd_hdim32_fp16_causal_sm80.cu` — 深入前向传播
- **反向传播：已完成**
- **前向传播进度：**
  ```
  fwd hdim256: bf16-causal ✓, bf16 ✓, fp16-causal ✓, fp16 ✓
  fwd hdim32:  bf16-causal ✓, bf16 ✓, fp16-causal (构建中), fp16 (待处理)
  fwd hdim128: 全部4个待处理
  fwd hdim192: 全部4个待处理
  ```

约剩余9个前向kernel。每个约1分钟，**约剩余10分钟**。