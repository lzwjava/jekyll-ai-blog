---
audio: false
generated: true
image: false
lang: en
layout: post
title: Galaxy GAMER II DDR4-2666 Recommended
translated: false
type: note
---

Question: Is the **Galaxy GAMER II DDR4-2666 8GB** a good match for your B150M + i5-6500 GPU test workstation?

Answer: **Yes. I would buy it, provided the price is reasonable.**

### Compatibility

Your setup:

```text
MSI B150M
    +
i5-6500
    +
Galaxy GAMER II DDR4-2666 8GB
```

**Compatible.** The important point is that DDR4-2666 will simply **downclock to the platform's supported memory speed** (DDR4-2133 with the i5-6500/B150 platform).

So:

```text
RAM stick:       DDR4-2666
       ↓
B150 + i5-6500
       ↓
Runs at ~DDR4-2133
```

You don't get 2666 MHz, but that's completely fine for GPU testing.

### 1×8GB is exactly what I'd use

For your workstation:

| Configuration | Verdict     |
| ------------- | ----------- |
| 1×4GB         | ❌ I'd avoid |
| 2×4GB         | 👍 Fine     |
| **1×8GB**     | ⭐ **Best**  |
| 2×8GB         | Unnecessary |

You don't need dual-channel performance for GPU diagnosis. Your workload is more like:

```text
Boot Linux
→ NVIDIA driver
→ nvidia-smi
→ GPU-Z / lspci
→ CUDA test
→ VRAM test
→ stress test
→ benchmark
```

8 GB system RAM is plenty.

### One thing I'd check

"双面颗粒" is not a problem. **Don't confuse dual-sided memory with ECC/registered memory.**

Ask the seller for a CPU-Z screenshot showing:

```text
Type:       DDR4
Size:       8 GB
DRAM:       ...
Module:     UDIMM
```

If it's a normal desktop **DDR4 UDIMM**, you're good.

**My ranking now:**

> **B150M + i5-6500 ¥219 + this 8GB DDR4-2666 → very sensible cheap GPU test platform.**

The 2666 rating isn't wasted—it just gives you a stick that can also be reused in a newer DDR4 system later.
