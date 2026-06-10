---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attn Backward Compilation Progress
translated: false
type: note
---

Good progress:

- Compiling: `flash_bwd_hdim192_bf16` (backward, head dim 192, bf16)
- Extension: `flash_attn_2_cuda`
- 56 temp files generated so far
- Disk: 34GB free (stable)
- 3 active compile processes

It's working through the backward pass kernels now. Still got a ways to go — flash-attn has ~100+ kernel variants (fwd/bwd × fp16/bf16 × head dims 64/96/128/192/256). Should be done in ~20-40 min.
