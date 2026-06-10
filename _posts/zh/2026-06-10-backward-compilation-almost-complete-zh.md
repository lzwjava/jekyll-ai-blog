---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 反向编译几乎完成
translated: true
type: note
---

进展顺利：

- **已编译 15 个 .o 文件**（几分钟前仅为 2 个）
- **当前编译目标：** `flash_bwd_hdim32_fp16_causal_sm80.cu` — 接近反向阶段尾声
- **反向阶段：** 即将完成（所有 hdim 32/128/192/256 × fp16/bf16 × causal/non-causal 均已覆盖）
- **正向阶段：** 接下来进行

已编译的反向内核：
```
flash_api.o
反向 hdim128：bf16-causal、bf16、fp16-causal、fp16  ✓
反向 hdim192：bf16-causal、bf16、fp16-causal、fp16  ✓
反向 hdim256：bf16-causal、bf16、fp16-causal、fp16  ✓
反向 hdim32： bf16-causal、bf16  ✓、fp16-causal（编译中）、fp16（待处理）
```

每个 .o 文件约需 1 分钟，单架构构建。正向阶段约有 16 个内核，预计剩余时间约 15-20 分钟。