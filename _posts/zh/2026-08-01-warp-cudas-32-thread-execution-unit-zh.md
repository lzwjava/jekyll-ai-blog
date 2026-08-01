---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp：CUDA的32线程执行单元
translated: true
type: note
---

问题：在 vLLM / LLM 推理的上下文中，“warp”是什么意思？

答案：这是一个纯粹的 CUDA 硬件概念，并非 vLLM 发明的——vLLM 的内核只是大量使用了它。

**Warp = 在一个 SM (Streaming Multiprocessor) 上以锁步方式执行的 32 个线程。**

- 它是 NVIDIA GPU 上实际的调度单元。你不会启动“32 个线程”，而是启动一个线程块，硬件将其分割成 32 个线程的 warp。
- warp 中的所有 32 个线程同时执行*相同的指令*（SIMT —— Single Instruction, Multiple Threads）。如果 warp 中的线程发生分歧（不同的 `if` 分支），warp 会串行化两条路径——“warp divergence”，这是一个真正的性能杀手。
- warp 内的线程可以通过 warp 级原语（如 `__shfl_down_sync`、`__shfl_xor_sync`）廉价地相互通信——不需要经过共享内存。这用于快速规约（例如，在一个 warp 内进行 softmax 求和/取最大值）。

为什么这在 vLLM 中特别重要——warp 是一组 32 个线程，它们在一个流多处理器上同时执行，在 PagedAttention 内核中，每个 warp 一次处理一个查询 token 与一个完整 KV 缓存块中 key token 之间的计算。如果对于一个上下文有 4 个 warp 和 6 个块，warp 0 处理块 0 和 4，warp 1 处理块 1 和 5，warp 2 处理块 2，warp 3 处理块 3——因此 warp 以 round-robin 方式分配 KV 块。

内核中的层次结构：**thread → warp (32 threads) → thread block (multiple warps, shared memory) → grid (blocks × heads × seqs)**。

代码中的最小思维模型：

```cuda
// 概念上每个 PagedAttention 在每个 warp 中所做的操作
__global__ void paged_attention_kernel(...) {
    int warp_id = threadIdx.x / WARP_SIZE;  // WARP_SIZE = 32
    int lane_id = threadIdx.x % WARP_SIZE;  // 在 warp 中的位置

    for (block = warp_id; block < num_blocks; block += NUM_WARPS) {
        // 这个 warp 计算其分配的 KV 块的 QK^T
        // 然后进行 warp 级规约 (__shfl_down_sync) 用于 softmax
    }
}
```

如果你正在阅读 FlashAttention 4 的源代码，这也相关：它将流水线的块映射到称为 warp 的 32 线程组，这种技术称为 warp specialization —— 同一个块中的不同 warp 并发地做不同的工作（加载、计算、写入），而不是都做同样的事情，以重叠 memory 和 compute。

而 DeepSeek 较新的 vLLM 内核更进一步：一个 fused kernel 使用静态的 warpID dispatch，每个 warp 独立处理一个 Q head 或一个 K head，因此不需要跨 warp 通信。

TL;DR：如果你正在阅读 vLLM/FlashAttention 内核源代码（`csrc/attention/*.cu`），“warp”只是 CUDA 的 32 线程执行单元——这个抽象决定了工作如何在 query tokens / KV blocks / heads 上进行分块以实现最大并行性。

参考：

- [vLLM PagedAttention 设计文档](https://docs.vllm.ai/en/latest/design/paged_attention/)
- [我们对 Flash Attention 4 进行了逆向工程](https://modal.com/blog/reverse-engineer-flash-attention-4)
- [DeepSeek V4 在 vLLM 中：高效的长上下文注意力](https://vllm.ai/blog/2026-04-24-deepseek-v4)
