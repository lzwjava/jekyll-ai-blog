---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning Through Hardware Adaptation
translated: false
type: note
---

**Question:** If DeepSeek can adapt to domestic Chinese chips, why can't I adapt to AMD? The process is slow (6–12 months), but DeepSeek's team deepened their GPU/chip understanding through it. Is that why Liang Wenfeng led DeepSeek to do the native chip adaptation?

**Answer:**

Yes, exactly right. And this is one of the most underrated strategic insights in the current AI landscape.

## The Real Reason DeepSeek Did Native Chip Adaptation

Liang Wenfeng has been explicit about this. The Huawei Ascend / domestic chip adaptation wasn't just a compliance move — it was a **forcing function for deep systems understanding**.

When you can't rely on CUDA abstractions, you're forced to understand:

- **Memory hierarchy** at the hardware level (HBM bandwidth, SRAM tiling, cache locality)
- **Compute primitives** — what the hardware actually executes, not what PyTorch pretends it does
- **Kernel fusion** — why naively chaining ops is slow, how to write fused kernels
- **Quantization at the hardware level** — INT8/FP8 in terms of actual tensor core utilization
- **Communication collectives** — NCCL equivalents, all-reduce, ring topologies across non-NVIDIA interconnects

DeepSeek's team didn't just "port" to Ascend. They **rebuilt intuitions** about how transformers map to silicon. That's why their architecture innovations (MLA, MoE with expert parallelism, FP8 training) are so hardware-aware — they came from people who had fought with the metal directly.

## Why You Should Do the Same with AMD

The analogy is clean:

| DeepSeek situation | Your situation |
|---|---|
| NVIDIA H100 → Huawei Ascend | NVIDIA CUDA → AMD ROCm |
| Forced to understand Ascend ISA | Forced to understand GCN/RDNA/CDNA |
| Built custom kernels in CANN | Build custom kernels in HIP/Triton |
| Gained hardware-level intuition | Same outcome |

AMD ROCm is actually **less painful** than Ascend adaptation because:
- HIP is syntactically near-identical to CUDA
- PyTorch ROCm support is solid (MI300X is now a first-class target)
- Triton works on AMD via the ROCm backend

## What You'd Actually Learn

```python
# On NVIDIA, you write this and forget about it:
torch.matmul(a, b)  # cuBLAS handles everything

# On AMD, when things break, you trace into:
# rocBLAS → hipBLAS → actual GCN wavefront scheduling
# You learn: wavefront size (64 on AMD vs 32 warp on NVIDIA)
# LDS (local data share) vs NVIDIA shared memory
# Why occupancy calculations differ
```

Concrete skills you'd compound:

1. **Triton kernel writing on AMD** — same language, different backend, forces you to understand why your tiling strategy matters
2. **ROCm profiler (`rocprof`)** — equivalent to Nsight, teaches you to read hardware counters
3. **CDNA architecture** (MI300X) — unified CPU+GPU memory, 192GB HBM3, relevant for inference at scale
4. **HIP porting patterns** — mechanical but teaches CUDA internals by contrast

## The Compounding Argument

Liang Wenfeng's bet: short-term pain (slower dev velocity) → long-term moat (team that understands the full stack).

For you specifically: you're already training GPT-2 on H100s. You have the NVIDIA intuition baseline. Adding AMD/ROCm gives you:

- **Cross-architecture mental model** — you stop thinking "CUDA" and start thinking "GPU compute"
- **Differentiation** — most AI engineers only know CUDA; AMD fluency is genuinely rare
- **Relevance** — AMD MI300X is being deployed at scale (Microsoft, Meta); ROCm is no longer a toy

## Practical Starting Point

```bash
# If you have any AMD GPU access (even a gaming GPU):
pip install torch --index-url https://download.pytorch.org/whl/rocm6.1

# Verify:
python -c "import torch; print(torch.cuda.is_available())"  # shows True on ROCm too
python -c "import torch; print(torch.version.hip)"

# Run your existing GPT-2 training script — see what breaks
# Every error is a lesson in where CUDA and ROCm diverge
```

The 6–12 month timeline you mentioned is real, but the payoff is exactly what you identified: **hardware-level intuition that most AI engineers never develop because they never leave the NVIDIA comfort zone.**

DeepSeek's chip adaptation story is essentially: *constraints are curriculum*. The same logic applies to you.
