---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Torch 编译阶段与训练估算
translated: true
type: note
---

这里有两个阶段：

1. **iter 0: 113s** — `torch.compile()` 正在 tracing/optimizing the graph。这是一个一次性成本。
2. **iter 50: 21s** — 已编译并运行

编译完成后，你应该稳定在 **1-3 sec/step** 左右。164% MFU 看起来很奇怪 — 很可能是在编译期间的测量伪影。

**时间估计：**
- 剩余 ~100,000 iters
- 如果编译后 ~2 sec/step → **~56 hours** (~2.3 days)
- 如果 21 sec/step 持续 → **~24 days** ← 这会很糟糕

现在检查 `nvidia-smi` — GPU-Util 还是 100% 吗？如果是，只是编译开销。一旦完成，你会看到巨大的加速。

另外 — loss 从 11.05 → 7.65（在 50 steps 内）下降是健康的。模型学习良好。问题是它是否会加速。
