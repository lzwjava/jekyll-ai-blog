---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Radeon Pro VII ¥630 Deal
translated: false
type: note
---

## Question: Is an AMD Radeon Pro VII at ¥630 CNY from Xianyu a good deal?

## Answer

Yes. **¥630 CNY for a working AMD Radeon Pro VII 16GB HBM2 is a very attractive price**, especially because this is not just an old gaming GPU — it is basically a workstation/HPC card with HBM2 + ECC. Used Radeon Pro VII cards are often listed much higher internationally; for example, used listings around several hundred USD exist, although those markets are not directly comparable to Xianyu. ([eBay][1])

For your situation (AI experiments + cheap GPU cluster), I would rate it:

```
Value:
Hardware:        9/10
AI ecosystem:    5/10
Learning value:  10/10
Risk:            medium
```

---

### Why ¥630 is interesting

At ¥630:

```
Radeon Pro VII

16GB HBM2
ECC
~1 TB/s memory bandwidth
Vega 20
PCIe 4.0
Display output
```

You are basically buying:

```
MI50-like compute
+
a workstation card
+
a display output
```

The closest comparison:

| GPU            | Used price | VRAM       | Memory bandwidth |
| -------------- | ---------- | ---------- | ---------------- |
| RTX 3060 12GB  | ~¥1500     | 12GB GDDR6 | ~360 GB/s        |
| RTX 4070       | ~¥4000     | 12GB       | ~500 GB/s        |
| Radeon Pro VII | ¥630       | 16GB HBM2  | ~1 TB/s          |

The silicon is very interesting.

---

### Compared with your MI50 plan

Actually this is arguably better for a home lab.

MI50:

```
No display
Server card
Need iGPU/second GPU
```

Pro VII:

```
Mini DP output
Normal workstation card
Can boot Linux directly
```

Your machine:

```
Ryzen 5600
B550
32GB RAM
Radeon Pro VII
Ubuntu
ROCm experiments
```

is much easier to operate.

---

### But the important warning: AI software

The GPU itself is not the problem.

The problem is:

```
modern AI stack
        |
        v
CUDA-first world
```

For example:

```
vLLM        ❌ difficult
TensorRT    ❌ NVIDIA only
FlashAttn   ❌ difficult
CUDA kernels ❌
```

ROCm:

```
PyTorch     ✅ possible
HIP         ✅ possible
llama.cpp   ✅ possible
custom GPU  ✅ educational
```

Vega 20 support is old, and community experience shows that newer ROCm versions may require extra work on gfx906 cards like Radeon VII/MI50. ([Reddit][2])

---

### Before buying, ask seller for

1. GPU-Z screenshot (Windows)

Need:

```
GPU: Radeon Pro VII
Memory: HBM2 16384 MB
Bus: PCIe x16
```

2. Run:

```
FurMark 10 minutes
```

Check:

* no artifacts
* temperature <95°C
* fans normal

3. Photo:

* Mini DisplayPort works
* PCIe gold fingers clean
* no burned PCB

---

### My decision if I were you

For ¥630:

I would buy it.

Because your goal is not only "maximum tokens/sec". You are building understanding:

```
CUDA
  |
ROCm
  |
GPU architecture
  |
distributed training
```

You already have RTX 4070 for practical CUDA work.

This Pro VII becomes your "AMD research node":

```
RTX 4070
    |
    | CUDA
    |
production experiments


Radeon Pro VII
    |
    | ROCm/HIP
    |
hardware exploration
```

For an AI engineer building infrastructure, this is more valuable than another ordinary gaming GPU.

References:

* ([eBay][1])
* ([Reddit][2])

[1]: https://www.ebay.com/itm/406763510835?utm_source=chatgpt.com "AMD Radeon Pro VII 16GB HBM2 Graphics Card Workstation GPU | eBay"
[2]: https://www.reddit.com/r/homelabsales/comments/1q5cn0o/fsusca_radeon_pro_vii/?utm_source=chatgpt.com "[FS][US-CA] Radeon Pro VII"
