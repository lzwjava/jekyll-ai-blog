---
audio: false
generated: true
image: false
lang: en
layout: post
title: Profiling GPU and Managing Inference Trade-offs
translated: false
type: note
---

Question: How do I profile GPU bottlenecks, manage CUDA memory, and choose between batch and real-time inference?

Answer:

**1. Profiling GPU bottlenecks**

Work top-down: system level first, then kernel level.

- **Check utilization.** Run `nvidia-smi dmon` or `nvtop`. Low GPU utilization with a busy CPU usually means a data-loading or launch-overhead bottleneck, not a compute one.
- **Timeline profiling (Nsight Systems).** Run `nsys profile -o report python infer.py`. Look for:
  - Gaps between kernels, which point to CPU-side overhead, Python overhead, or synchronization.
  - Host-to-device copies that block compute. Use pinned memory and `non_blocking=True`.
  - Frequent `cudaDeviceSynchronize` calls, often caused by `.item()`, `.cpu()`, or printing tensors in the hot path.
- **Kernel profiling (Nsight Compute).** Run `ncu` on the hottest kernels and check whether each is memory-bound or compute-bound using the roofline and SOL (speed-of-light) metrics. Memory-bound kernels benefit from fusion, lower precision, and better access patterns. Compute-bound kernels benefit from Tensor Cores (FP16/BF16/FP8) and better tiling.
- **Framework-level profiling.** In PyTorch, use `torch.profiler` with `record_shape=True` and `profile_memory=True`, and view the trace in TensorBoard or Perfetto. Add `torch.cuda.nvtx.range_push/pop` markers to correlate with Nsight.
- **Common fixes.** Use CUDA Graphs or `torch.compile` to cut launch overhead, fuse operators, use TensorRT or vLLM-style engines for serving, and overlap copy and compute with multiple streams.

**2. Managing CUDA memory**

- **Measure it.** Use `torch.cuda.memory_allocated()`, `memory_reserved()`, `max_memory_allocated()`, and `torch.cuda.memory_summary()`. For deeper inspection, use `torch.cuda.memory._record_memory_history()` and the memory snapshot visualizer.
- **Understand the caching allocator.** PyTorch keeps freed blocks reserved, so `nvidia-smi` shows more than your live tensors. Fragmentation is the usual cause of OOM when total free memory looks sufficient. Mitigate with `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` or by tuning `max_split_size_mb`. Avoid calling `empty_cache()` in hot loops because it hurts performance.
- **Reduce the footprint.**
  - Use `torch.inference_mode()` or `no_grad`.
  - Use FP16/BF16/FP8, or INT8/INT4 quantization.
  - Share or reuse buffers and preallocate static shapes. Padding to fixed buckets lowers fragmentation.
  - For LLMs, manage the KV cache carefully with paged attention, as in vLLM, and cap context length and concurrency.
- **Avoid leaks.** Don't keep references to GPU tensors in logs or lists. Detach and move to CPU before storing.
- **Multi-model serving.** Isolate models per process or use MPS/MIG for predictable memory partitioning.

**3. Batch vs. real-time inference trade-offs**

| Aspect | Batch / offline | Real-time / online |
|---|---|---|
| Goal | Maximize throughput and cost efficiency | Minimize per-request latency (p95/p99) |
| Batch size | Large, saturates the GPU | Small (1 to a few) or dynamically formed |
| GPU utilization | High | Often low unless batched cleverly |
| Memory | Larger activations allowed | Tight, needs headroom for spikes |
| Cost per request | Lowest | Higher |

Strategies for the middle ground:

- **Dynamic batching.** Hold requests for a short window (for example 1 to 10 ms) to form batches, bounded by a latency SLO. Triton's dynamic batcher does this with `max_queue_delay_microseconds` and preferred batch sizes.
- **Continuous (in-flight) batching.** For autoregressive LLMs, new requests join the batch at each decoding step instead of waiting for the whole batch to finish. This greatly improves throughput at similar latency.
- **Separate workloads.** Run latency-critical traffic on dedicated instances or MIG slices. Run bulk jobs on separate capacity or off-peak.
- **Tune with a load test.** Sweep batch size and concurrency, then plot throughput against p99 latency to find the knee of the curve, and pick the largest batch that still meets your SLO.
- **Latency tools.** Use CUDA Graphs, TensorRT engines, model warmup, static shapes, and keeping models resident in GPU memory to avoid cold starts.
- **Rule of thumb.** If the SLO is loose (seconds or more), favor large batches. If it is tight (tens of ms), use small dynamic batches with warm, optimized engines, and accept lower utilization.

References:
- [NVIDIA Nsight Systems documentation](https://docs.nvidia.com/nsight-systems/)
- [NVIDIA Nsight Compute documentation](https://docs.nvidia.com/nsight-compute/)
- [PyTorch Profiler recipe](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
- [PyTorch CUDA semantics (memory management)](https://pytorch.org/docs/stable/notes/cuda.html)
- [Triton Inference Server documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/)
- [vLLM documentation](https://docs.vllm.ai/)