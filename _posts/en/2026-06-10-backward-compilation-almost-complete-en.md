---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backward Compilation Almost Complete
translated: false
type: note
---

Progress looks good:

- **15 .o files compiled** (was 2 a few min ago)
- **Currently on:** `flash_bwd_hdim32_fp16_causal_sm80.cu` — near end of backward pass
- **Backward pass:** almost done (all hdims 32/128/192/256 × fp16/bf16 × causal/non-causal)
- **Forward pass:** still coming next

Backward kernels compiled:

```
flash_api.o
bwd hdim128: bf16-causal, bf16, fp16-causal, fp16  ✓
bwd hdim192: bf16-causal, bf16, fp16-causal, fp16  ✓
bwd hdim256: bf16-causal, bf16, fp16-causal, fp16  ✓
bwd hdim32:  bf16-causal, bf16  ✓, fp16-causal (building), fp16 (pending)
```

~1 min per .o file, single-arch build. Forward pass has ~16 kernels. Estimate ~15-20 min remaining.
