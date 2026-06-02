---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X 760M Model Training Estimate
translated: false
type: note
---

**Estimated training time for 760M on 14.6B tokens, single MI300X: ~24-35 hours**

Here's the breakdown:

```
Total FLOPs:     6.66 × 10^19
MI300X peak:     1,307 TFLOPS (bf16)
Realistic MFU:   40-60% (single GPU, no communication overhead)

At 40% MFU:  ~35 hours
At 50% MFU:  ~28 hours  ← most likely
At 60% MFU:  ~24 hours
```

**Cross-validation with Karpathy's nanochat:**

- d24 (~1.5B) on 8×H100: ~2 hours for 4.64e18 FLOPs
- Our run: 6.66e19 FLOPs = 14× more compute
- On 8×H100: 14 × 2 = 28 hours
- On 1×MI300X (1.33× faster than H100): ~21 hours
- Account for single-GPU overhead: **~24-28 hours**

**Comparison with your 124M model on RTX 4070:**

- 124M on 4070, 10B tokens: ~15-20 hours
- 760M is 6.1× more FLOPs/token
- MI300X is ~10.5× faster (bandwidth-bound case)
- Net: 15-20 × 6.1 × (14.6/10) / 10.5 ≈ **13-17 hours** (if bandwidth-limited)
- But 760M is compute-bound → closer to **24-28 hours**

**Bottom line:** ~1-1.5 days on a single MI300X. Not bad for 14.6B tokens through a 760M model. You could start it in tmux and come back tomorrow.
