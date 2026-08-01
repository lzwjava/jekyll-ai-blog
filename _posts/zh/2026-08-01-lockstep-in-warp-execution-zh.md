---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp执行中的锁步
translated: true
type: note
---

问题：在 warp 执行上下文中，“lockstep”是什么意思？

答案：一个 warp 中的所有 32 个线程共享 **一个 instruction pointer / program counter**。硬件取指并解码单条指令，然后同时将其分发给所有 32 个线程——每个线程只在自己的数据（不同的寄存器、不同的内存地址）上运行相同的指令。这就是 SIMT：Single Instruction, Multiple Threads。“Lockstep”意味着在一个 warp 内，它们永远不可能同时处于不同的指令处。

与 CPU 线程池对比：32 个 CPU 线程可以各自处于完全不同的代码行，由操作系统独立调度。而 warp 不能——它是一个指令流，32 条数据通道。

**这在哪里会咬到你：branch divergence**

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

如果一个 warp 中线程 0-15 走路径 A，线程 16-31 走路径 B，那么 warp 并**不会**并行运行这两半。它会先执行路径 A，此时线程 16-31 被屏蔽（闲置），然后执行路径 B，线程 0-15 被屏蔽。总时间 = time(A) + time(B)，即使每次只有 16 个线程是“有用的”。这就是为什么 warp 内的 branch divergence 是一个经典的 GPU 性能陷阱——你需要串行支付两条路径的开销。

**为什么 warp 级别的 shuffle 因 lockstep 而有效**

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

这里你不需要一个 barrier，因为 lockstep *就是* barrier——warp 中的每个线程保证已经处于同一条指令。这正是 PagedAttention/FlashAttention 内核中用于跨 warp 低开销求和/求最大值的 softmax-reduction 技巧。

对于较新的 GPU（Volta+）有一个注意事项：线程在技术上现在拥有独立的 program counter（独立线程调度），所以 lockstep 不再是 100% 物理上保证的——但*调度模型*默认仍然将它们分组并一起执行，而 `_sync` 原语（`__shfl_down_sync`、`__syncwarp`）恰恰是为了在你需要时显式重新建立 lockstep 行为而存在的。
