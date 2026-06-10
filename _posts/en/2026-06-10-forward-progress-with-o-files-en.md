---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forward Progress with O Files
translated: false
type: note
---

Looking great:

- **26 .o files** compiled (was 15)
- **Currently:** `flash_fwd_hdim32_fp16_causal_sm80.cu` — deep into forward pass
- **Backward pass: DONE**
- **Forward pass progress:**
  ```
  fwd hdim256: bf16-causal ✓, bf16 ✓, fp16-causal ✓, fp16 ✓
  fwd hdim32:  bf16-causal ✓, bf16 ✓, fp16-causal (building), fp16 (pending)
  fwd hdim128: all 4 pending
  fwd hdim192: all 4 pending
  ```

~9 forward kernels left. At ~1 min each, **~10 min remaining**.
