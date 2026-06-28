---
audio: false
generated: true
image: false
lang: en
layout: post
title: B200 Compute Capability Is sm_100
translated: false
type: note
---

Question: Is the NVIDIA B200 compute capability sm_80?

Answer:

No. The B200 (Blackwell datacenter) is **sm_100** (compute capability 10.0).

Quick mapping of the relevant architectures:

| GPU | Arch | Compute Capability | `-arch` flag |
|-----|------|-------------------|--------------|
| A100 | Ampere | 8.0 | `sm_80` |
| RTX 30xx | Ampere | 8.6 | `sm_86` |
| RTX 40xx (your 4070) | Ada Lovelace | 8.9 | `sm_89` |
| H100 / H200 | Hopper | 9.0 | `sm_90` / `sm_90a` |
| B100 / B200 | Blackwell | 10.0 | `sm_100` / `sm_100a` |
| RTX 50xx (consumer Blackwell) | Blackwell | 12.0 | `sm_120` |

So `sm_80` is the **A100** (and other GA100-class parts). The B200 needs `sm_100`, which requires CUDA 12.8+ to compile for.

Note the consumer/datacenter Blackwell split: datacenter B200 is `sm_100`, but consumer RTX 50-series Blackwell is `sm_120` — different feature sets (e.g. the `a` variants like `sm_100a` expose arch-specific features like the 5th-gen Tensor Core / tcgen05 instructions used in cutting-edge GEMM kernels).

If you're compiling for B200 on the MI300X box — you can't, that's AMD/ROCm. For the AMD MI300X the equivalent target is `gfx942`.
