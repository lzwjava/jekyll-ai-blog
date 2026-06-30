---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PTX: Parallel Thread Execution"
translated: false
type: note
---

Question: What does PTX mean in the context of "This compiles down to optimized PTX without you touching shared memory, warp scheduling, or memory coalescing logic"?

Answer:

PTX = **Parallel Thread Execution** — NVIDIA's intermediate representation (IR) for GPU code, analogous to LLVM IR in the CPU compiler world.

The actual compilation pipeline:

```
CUDA C++ / Triton / torch.compile
        │  (nvcc / Triton compiler frontend)
        ▼
      PTX (virtual ISA, human-readable assembly-like)
        │  (ptxas — PTX assembler, happens at install/runtime)
        ▼
    SASS (real machine code, GPU-architecture-specific, e.g. sm_90 for Hopper, sm_94/sm_90a for H100)
```

Key properties:

- **PTX is virtual, not physical.** It's not tied to a specific GPU SKU — `ptxas` JIT-compiles PTX to SASS for whatever GPU is actually present at runtime. This is why a single `.so` shipped with PTX embedded can run on multiple GPU generations (forward compatibility), unlike raw SASS which is architecture-locked.
- **It's where the high-level scheduling decisions get baked in.** When you write Triton or use `torch.compile`, the compiler decides register allocation, instruction selection, and a first pass at thread/warp mapping when lowering to PTX. `ptxas` then does further architecture-specific scheduling (instruction reordering, SASS-level optimizations) when going PTX → SASS.
- **You can inspect it directly**: `nvcc -ptx kernel.cu -o kernel.ptx`, or for Triton: `kernel.asm['ptx']`. For SASS: `cuobjdump --dump-sass kernel.cubin` or `nvdisasm`.

Since you're running on the MI300X too — AMD's equivalent isn't PTX, it's **GCN/CDNA ISA** directly via `hipcc`, or for the portable IR layer, **LLVM IR → AMDGPU backend**. ROCm doesn't have a separate virtual-ISA stage like PTX; HIP compiles closer to the metal, which is part of why HBM3 bandwidth tuning on MI300X is more hands-on than CUDA's "let ptxas figure it out" model.

Practical check worth doing on your 4070: compile a small kernel with `nvcc -arch=sm_89 -ptx`, read the `.ptx` file — you'll see `.reg`, `.shared`, `ld.global`, `st.shared` instructions. It's genuinely readable and is the fastest way to verify whether your Python/Triton code actually generated the memory access pattern you intended (coalesced `ld.global.v4` vs scattered scalar loads), rather than profiling blind with Nsight Compute first.
