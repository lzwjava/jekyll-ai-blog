---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nano-vLLM：精简版vLLM复现
translated: true
type: note
---

这个 agent 项目是 **nano-vllm** —— 用约 1,200 行 Python 从零重新实现的 vLLM serving engine。下面自上而下说明它的工作原理：

## 核心循环（LLMEngine → Scheduler → ModelRunner）

**1. 你调用 `llm.generate(prompts, sampling_params)`**（`llm.py` → `engine/llm_engine.py`）。它会：
- 把每个 prompt 分词成一个 `Sequence`
- 把它们放入 Scheduler 的等待队列
- 然后反复调用 `step()`，直到每个 sequence 都完成

**2. 每一次 `step()` 就是一次 GPU 前向传播，这也是系统的核心：**

```
uvloop:   step() -> scheduler.schedule() -> model_runner.run() -> scheduler.postprocess()
```

## 为什么快：continuous batching

朴素的服务实现一次只处理一个请求。nano-vllm 则把*许多* sequence 打包进一次前向传播：

- **Prefill 阶段** —— 新的 prompt token 会在一个打包好的 batch 中被处理（`prepare_prefill` 构建一个连续的 tensor）；scheduler 会贪心地填满到 `max_num_batched_tokens` 和 `max_num_seqs`。
- **Decode 阶段** —— 当没有等待中的请求时，每个运行中的 sequence 恰好贡献 **1 个 token**（`input_ids[i] = seq.last_token`），因此所有 sequence 并行推进。一旦某个 sequence 结束（`EOS` / `max_tokens`），它会被移出，下一个等待中的 sequence 会**立即被调度进来**（vLLM 的 continuous batching）——不需要等整个 batch 排空。

因此，一个 256 请求的 benchmark 会让它们全部并发运行，而不是串行运行。这就是它能在笔记本 4070 上达到约 1434 tok/s 的原因。

## PagedAttention：KV cache 分页

每个 sequence 不再使用一块连续的 KV buffer，而是让每一层的 KV cache 变成一个单一的全局 tensor：

```python
self.kv_cache = torch.empty(2, num_layers, num_blocks, block_size, num_kv_heads, head_dim)
```

每个 `Sequence` 都有一个 `block_table`（block ID 列表），类似于页表。`BlockManager` 跟踪空闲 block（`ref_count`、free list）。由此产生两个结果：

- **零碎片化** —— 一个已结束 sequence 的 block 可以立即被其他 sequence 复用，即使它的内容在位置 7771 结束。
- **Prefix caching** —— block 会保存一个滚动 `xxhash`（`hash_blocks`）。当新 prompt 到达时，`scheduler.can_allocate` 会检查已计算过的哈希：如果某个 prompt 与之前的一个 prompt 共享前缀，这些 block 会被**以 `ref_count += 1` 的方式复用**，且只计算后缀。这就是 `attention.py` 中的 `block_tables` / `_gather_kv_from_cache` 路径。

在 decode 过程中，runner 通过从分页 cache 中 *gather* 来读取完整历史，因此 attention 开销恰好与 sequence 长度成正比——这也是 decode 受内存带宽限制的原因。

## ModelRunner（`model_runner.py`）

这是唯一直接接触 GPU 的部分：

```python
dist.init_process_group("nccl", ...)       # Tensor parallelism (world_size ranks)
warmup_model()                              # dummy run to allocate workspace/mem pools
allocate_kv_cache()                         # sizes cache from free GPU mem * gpu_memory_utilization
capture_cudagraph()                         # unless enforce_eager
run()  -> prepare_prefill/decode + forward + sampler
```

下面这些关键优化对应真实 vLLM 的做法：

- **`prepare_prefill`** 会构建 `cu_seqlens_q/k`、`slot_mapping`、`block_tables`，因此一次 `flash_attn_varlen_func` 调用就能处理整个 ragged batch（包括带 prefix-cache 偏移的 causal mask）。
- **CUDA graphs** —— decode 前向传播会按 batch size 桶（`graph_bs = [1,2,4,8,16,...]`）被捕获到 `CUDAGraph` 中。Graph capture 消除了每个 token 的 Python/launch 开销；这里只使用不含 `.item()` 的路径，因为在捕获期间不允许出现条件分支（参见 `attention.py` 中的 `is_current_stream_capturing()` 分支）。
- **Chunked prefill** —— 单个过长的 prompt 不会饿死整个 batch；scheduler 会把 prefill 拆成多个 chunk（`only allow chunked prefill for the first seq`）。
- **Preemption** —— 如果 decode 没有空闲 block，scheduler 会按 LIFO 把正在运行的 sequence 逐出并送回 WAITING，同时释放它的 block。
- **Tensor parallelism** —— rank 0 通过共享内存 IPC（`SharedMemory` 中的 page-sized pickle）进行编排，workers 运行各自的分片；只有 rank 0 进行采样。
- **Pin-memory + `non_blocking=True`** 的 H2D 输入拷贝。

## 学习角度（来自 `AGENTS.md`）

这个仓库的重点不是“使用 vLLM”，而是*看清* serving 机制。`experiments/` 文件夹就是设计好的学习循环：

```bash
python3.12 experiments/04_scheduler_watch.py     # watch continuous batching live
python3.12 experiments/07_mixed_length_batch.py  # mixed-length batching
```

实验 1 就是那个“aha”时刻：decode 延迟随 prompt 长度线性增长（从 4 到 2048 个 token，31ms/tok → 1159ms/tok），因为 attention 每一步都会重读整个 KV cache——这正是 PagedAttention + batching 要解决的问题。这是推理系统领域里与 nanoGPT 损失曲线对应的类比。

注意环境细节：始终使用 `python3.12`（系统 `/usr/bin/python3.12`），绝不要用 `python3`，因为依赖目标版本是 `>=3.10,<3.13`。

需要我更详细地讲解某一部分吗——比如 scheduler 的 preemption 逻辑、CUDA graph capture，或 prefix caching 的哈希机制？