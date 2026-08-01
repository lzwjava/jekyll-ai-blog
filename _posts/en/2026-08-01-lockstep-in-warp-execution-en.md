---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lockstep in Warp Execution
translated: false
type: note
---

Question: What does "lockstep" mean in the context of warp execution?

Answer: All 32 threads in a warp share **one instruction pointer / program counter**. The hardware fetches and decodes a single instruction, then issues it to all 32 threads simultaneously — each thread just runs that same instruction on its own data (different registers, different memory addresses). That's SIMT: Single Instruction, Multiple Threads. "Lockstep" = they can never be at different instructions at the same time within a warp.

Contrast with a CPU thread pool: 32 CPU threads can each be at a completely different line of code, scheduled independently by the OS. A warp cannot — it's one instruction stream, 32 data lanes.

**Where this bites you: branch divergence**

```cuda
__global__ void kernel(int* data) {
    int tid = threadIdx.x;
    if (data[tid] > 0) {
        // path A
        do_work_a();
    } else {
        // path B
        do_work_b();
    }
}
```

If threads 0-15 in a warp take path A and threads 16-31 take path B, the warp does **not** run both halves in parallel. It executes path A with threads 16-31 masked off (idle), then executes path B with threads 0-15 masked off. Total time = time(A) + time(B), even though only 16 threads were "useful" in each pass. This is why divergent branches inside a warp are a classic GPU perf trap — you pay for both paths serially.

**Why warp-level shuffle works because of lockstep**

```cuda
// __shfl_down_sync relies on all threads hitting this instruction
// at the exact same cycle — that's what lockstep guarantees
val += __shfl_down_sync(0xffffffff, val, 16);
val += __shfl_down_sync(0xffffffff, val, 8);
val += __shfl_down_sync(0xffffffff, val, 4);
val += __shfl_down_sync(0xffffffff, val, 2);
val += __shfl_down_sync(0xffffffff, val, 1);
// lane 0 now holds sum of all 32 lanes — no shared memory, no __syncthreads()
```

You don't need a barrier here because lockstep *is* the barrier — every thread in the warp is guaranteed to be at the same instruction already. That's exactly the softmax-reduction trick used inside PagedAttention/FlashAttention kernels to sum/max across a warp cheaply.

One caveat for newer GPUs (Volta+): threads technically have independent program counters now (independent thread scheduling), so lockstep isn't 100% physically guaranteed anymore — but the *scheduling model* still groups them and executes them together by default, and `_sync` primitives (`__shfl_down_sync`, `__syncwarp`) exist precisely to explicitly re-establish lockstep behavior when you need it.
