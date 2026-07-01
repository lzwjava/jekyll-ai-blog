---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blackwell FP4 Inference vs AMD Training
translated: false
type: note
---

**Answer:**

Your friend is making a precise technical argument. Let me break it down:

**FP4 vs FP8 — the Blackwell differentiator:**

Blackwell's key hardware feature is native **FP4 tensor cores** (MX-FP4 / NVFP4). This is new — previous Hopper/Ada only went down to FP8.

```
Precision hierarchy:
FP32 → BF16 → FP16 → FP8 → FP4

Blackwell native support:
- FP4: ✅ hardware tensor cores (2x throughput vs FP8)
- FP8: ✅
- AMD MI300X: FP8 ✅, FP4 ❌ (software emulation only)
```

**Your friend's point exactly:**

| Use case | Recommended precision | Blackwell advantage |
| ---------- | ---------------------- | --------------------- |
| Inference | FP4 quantization | Huge — native FP4 ops |
| Training | FP8 | Moderate — both have it |
| Training | FP4 | ⚠️ risky — convergence issues |

**Why FP4 training is problematic:**

The representable range of FP4 is extremely narrow. During backprop, gradients can fall outside representable values → **gradient underflow/overflow → noisy updates → unstable convergence**. Your friend is right — FP8 is the practical floor for training. FP4 is inference-only in practice.

**The AMD angle:**

Your MI300X has excellent FP8 training (that's what DeepSeek used). But for **FP4 inference**, Blackwell wins cleanly — it's the hardware generation purpose-built for it.

**Summary of friend's advice:**

1. Blackwell's real edge = FP4 inference throughput
2. Training → FP8 is enough, FP4 adds noise risk
3. 24GB → too small, go bigger since you're already spending

Makes sense. If you buy Blackwell, you're buying for **inference speed at low precision** — that aligns with your agent/serving use cases more than training (you have MI300X for that).
