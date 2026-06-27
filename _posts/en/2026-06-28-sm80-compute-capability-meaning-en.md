---
audio: false
generated: true
image: false
lang: en
layout: post
title: SM80+ Compute Capability Meaning
translated: false
type: note
---

Question: What does NVIDIA SM80+ mean? Are SM versions like Apple's model numbers (e.g., A1728)?

Answer:

No — it's the opposite of an arbitrary marketing/model number. SM stands for **Streaming Multiprocessor architecture version**, and the number encodes the **compute capability** of the GPU. It's a structured, ordered version (major.minor), not a SKU identifier like Apple's `A1728`.

`SM80` = `sm_80` = compute capability **8.0**. The encoding is `SM<major><minor>`:

- `sm_70` → 7.0 → Volta (V100)
- `sm_75` → 7.5 → Turing (RTX 20xx, T4)
- `sm_80` → 8.0 → Ampere **datacenter** (A100)
- `sm_86` → 8.6 → Ampere **consumer** (RTX 30xx, your RTX 4070 is actually `sm_89`)
- `sm_89` → 8.9 → Ada Lovelace (RTX 40xx — **your 4070**)
- `sm_90` → 9.0 → Hopper (H100)
- `sm_100` → 10.0 → Blackwell (B100/B200)

Your MI300X is AMD, so it uses `gfx942` (CDNA3) instead — a totally separate ISA namespace.

**"SM80+" means compute capability ≥ 8.0.** It's a feature gate. Code or kernels marked SM80+ require hardware features introduced in Ampere, most importantly:

- **`cp.async`** — asynchronous global→shared memory copies (bypasses registers). This is what makes FlashAttention and modern GEMM pipelines fast.
- **3rd-gen Tensor Cores** with `bf16`, `tf32`, and async `mma` instructions.
- **Larger shared memory** (up to 164 KB/SM on A100).
- **Async barriers** (`mbarrier`).

This is why a lot of Triton/CUDA kernels (FlashAttention-2, many fused kernels) say "requires SM80+" — they emit `cp.async` PTX that simply doesn't exist on Turing.

The key difference from Apple model numbers: the ordering is **semantically meaningful and monotonic**. `sm_89 > sm_80` tells you Ada is a superset of Ampere features. `A1728 vs A1864` tells you nothing — they're just registry IDs.

Two practical wrinkles:

1. **Higher number ≠ strict superset.** `sm_86`/`sm_89` (consumer) are *newer* than `sm_80` (A100) but have **fewer Tensor Core FLOPs and less shared memory**. The minor version sometimes drops datacenter-only features. So "SM80+" guards a feature *baseline*, not a performance tier.

2. **Binary vs PTX.** When you compile CUDA you target either a real arch (`-arch=sm_89`, produces SASS binary) or a virtual arch (`-arch=compute_80`, produces PTX that JIT-compiles forward to newer GPUs). PyTorch ships fat binaries with `TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"`.

Quick check on your boxes:

```bash
# Your RTX 4070 → should print 8.9
nvidia-smi --query-gpu=compute_cap --format=csv,noheader

# In Python
python -c "import torch; print(torch.cuda.get_device_capability())"  # (8, 9)

# AMD MI300X — different namespace entirely
rocminfo | grep gfx   # gfx942
```

So: SM80 is to Apple model numbers as **semantic versioning is to a serial number**. The number *is* the capability spec.
