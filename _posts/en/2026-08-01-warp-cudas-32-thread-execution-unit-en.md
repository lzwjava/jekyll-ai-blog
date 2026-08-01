---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Warp: CUDA's 32-Thread Execution Unit"
translated: false
type: note
---

Question: What does "warp" mean in the context of vLLM / LLM inference?

Answer: It's a plain CUDA hardware concept, not something vLLM invented — vLLM's kernels just use it heavily.

**Warp = 32 threads that execute in lockstep on one SM (Streaming Multiprocessor).**

- It's the actual scheduling unit on NVIDIA GPUs. You don't launch "32 threads," you launch a thread block, and the hardware splits it into warps of 32.
- All 32 threads in a warp execute the *same instruction* at the same time (SIMT — Single Instruction, Multiple Threads). If threads in a warp diverge (different `if` branches), the warp serializes both paths — "warp divergence," a real perf killer.
- Threads within a warp can talk to each other cheaply via warp-level primitives like `__shfl_down_sync`, `__shfl_xor_sync` — no shared memory round-trip needed. This is used for fast reductions (e.g. softmax sum/max across a warp).

Why it matters in vLLM specifically — a warp is a group of 32 threads that execute simultaneously on a stream multiprocessor, and in the PagedAttention kernel each warp processes the calculation between one query token and key tokens of one entire KV cache block at a time. If there are 4 warps and 6 blocks for one context, warp 0 handles blocks 0 and 4, warp 1 handles blocks 1 and 5, warp 2 handles block 2, warp 3 handles block 3 — so warps get assigned KV blocks round-robin.

Hierarchy in the kernel: **thread → warp (32 threads) → thread block (multiple warps, shared memory) → grid (blocks × heads × seqs)**.

Minimal mental model in code:

```cuda
// conceptually what PagedAttention does per warp
__global__ void paged_attention_kernel(...) {
    int warp_id = threadIdx.x / WARP_SIZE;  // WARP_SIZE = 32
    int lane_id = threadIdx.x % WARP_SIZE;  // position within warp

    for (block = warp_id; block < num_blocks; block += NUM_WARPS) {
        // this warp computes QK^T for its assigned KV block
        // then does a warp-level reduction (__shfl_down_sync) for softmax
    }
}
```

Also relevant if you're reading FlashAttention 4 source: it maps chunks of the pipeline onto 32-thread groups called warps, a technique called warp specialization — different warps in the same block do different jobs (loading, computing, writing) concurrently instead of all doing the same thing, to overlap memory and compute.

And DeepSeek's newer vLLM kernels push this further: a fused kernel uses static warpID dispatch where each warp works independently on either a Q head or a K head, so no cross-warp communication is needed.

TL;DR: if you're reading vLLM/FlashAttention kernel source (`csrc/attention/*.cu`), "warp" is just CUDA's 32-thread execution unit — the abstraction that decides how work gets tiled across query tokens / KV blocks / heads for max parallelism.

References:

- [vLLM PagedAttention design doc](https://docs.vllm.ai/en/latest/design/paged_attention/)
- [We reverse-engineered Flash Attention 4](https://modal.com/blog/reverse-engineer-flash-attention-4)
- [DeepSeek V4 in vLLM: Efficient Long-context Attention](https://vllm.ai/blog/2026-04-24-deepseek-v4)
