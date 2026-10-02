---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU性能分析及推理权衡管理
translated: true
type: note
---

问题：如何分析 GPU 瓶颈、管理 CUDA 内存，以及在批量推理与实时推理之间进行选择？

答案：

**1. 分析 GPU 瓶颈**

自上而下分析：先系统层面，再内核层面。

- **检查利用率。** 运行 `nvidia-smi dmon` 或 `nvtop`。GPU 利用率低而 CPU 繁忙通常意味着数据加载或启动开销是瓶颈，而非计算本身。
- **时间线分析 (Nsight Systems)。** 运行 `nsys profile -o report python infer.py`。关注：
  - 内核之间的间隙，这通常指向 CPU 端开销、Python 开销或同步问题。
  - 阻塞计算的主机到设备 (Host-to-Device) 拷贝。应使用 Pinned Memory 和 `non_blocking=True`。
  - 频繁的 `cudaDeviceSynchronize` 调用，通常由在热路径中使用 `.item()`、`.cpu()` 或打印张量导致。
- **内核分析 (Nsight Compute)。** 运行 `ncu` 分析最热的内核，使用 Roofline 和 SOL (Speed-of-Light) 指标判断其是受内存限制还是受计算限制。受内存限制的内核可从算子融合、降低精度和更好的访问模式受益。受计算限制的内核可从 Tensor Cores (FP16/BF16/FP8) 和更好的分块受益。
- **框架级分析。** 在 PyTorch 中，使用带有 `record_shape=True` 和 `profile_memory=True` 参数的 `torch.profiler`，并在 TensorBoard 或 Perfetto 中查看跟踪。添加 `torch.cuda.nvtx.range_push/pop` 标记以与 Nsight 关联。
- **常见修复方法。** 使用 CUDA Graphs 或 `torch.compile` 来减少启动开销，融合算子，使用 TensorRT 或 vLLM 风格引擎进行服务，并通过多个流使拷贝与计算重叠。

**2. 管理 CUDA 内存**

- **进行测量。** 使用 `torch.cuda.memory_allocated()`、`memory_reserved()`、`max_memory_allocated()` 和 `torch.cuda.memory_summary()`。如需深入检查，请使用 `torch.cuda.memory._record_memory_history()` 和内存快照可视化工具。
- **理解缓存分配器。** PyTorch 会保留释放的块，因此 `nvidia-smi` 显示的内存会多于实际的活动张量。当总空闲内存看似充足时，碎片化通常是 OOM 的罪魁祸首。可以通过设置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 或调整 `max_split_size_mb` 来缓解。避免在热循环中调用 `empty_cache()`，因为它会损害性能。
- **减少内存占用。**
  - 使用 `torch.inference_mode()` 或 `no_grad`。
  - 使用 FP16/BF16/FP8，或 INT8/INT4 量化。
  - 共享或重用缓冲区，并预分配静态形状。填充到固定桶可降低碎片化。
  - 对于 LLM，通过分页注意力机制（如 vLLM 所做的那样）仔细管理 KV 缓存，并限制上下文长度和并发数。
- **避免泄漏。** 不要在日志或列表中保留对 GPU 张量的引用。在存储前先将其分离并移动到 CPU。
- **多模型服务。** 每个进程隔离模型，或使用 MPS/MIG 实现可预测的内存分区。

**3. 批量推理与实时推理的权衡**

| 对比维度 | 批量 / 离线 | 实时 / 在线 |
|---|---|---|
| 目标 | 最大化吞吐量和成本效率 | 最小化单次请求延迟 (p95/p99) |
| 批量大小 | 大，占满 GPU | 小（1 个或少数几个）或动态形成 |
| GPU 利用率 | 高 | 通常较低，除非巧妙地进行批处理 |
| 内存 | 允许较大的激活值 | 紧张，需要为峰值预留空间 |
| 每请求成本 | 最低 | 较高 |

折中策略：

- **动态批处理。** 将请求保留一个短窗口（例如 1 到 10 毫秒）以形成批次，受延迟 SLO 的限制。Triton 的动态批处理器通过 `max_queue_delay_microseconds` 和首选批量大小实现此功能。
- **连续（飞行中）批处理。** 对于自回归 LLM，新请求在每个解码步骤加入批次，而不是等待整个批次完成。这能在类似延迟下大幅提高吞吐量。
- **分离工作负载。** 在专用实例或 MIG 切片上运行延迟关键型流量。批量任务在单独资源或非高峰时段运行。
- **通过负载测试进行调优。** 扫描批量大小和并发数，然后绘制吞吐量与 p99 延迟的关系图，找到曲线拐点，并选择在满足 SLO 的前提下可使用的最大批量。
- **延迟优化工具。** 使用 CUDA Graphs、TensorRT 引擎、模型预热、静态形状，并将模型常驻 GPU 内存以避免冷启动。
- **经验法则。** 如果 SLO 宽松（数秒或更长），倾向于大批量。如果 SLO 严格（数十毫秒），使用带有预热、优化引擎的小型动态批量，并接受较低的利用率。

参考资料：
- [NVIDIA Nsight Systems 文档](https://docs.nvidia.com/nsight-systems/)
- [NVIDIA Nsight Compute 文档](https://docs.nvidia.com/nsight-compute/)
- [PyTorch Profiler 教程](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
- [PyTorch CUDA 语义（内存管理）](https://pytorch.org/docs/stable/notes/cuda.html)
- [Triton Inference Server 文档](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/)
- [vLLM 文档](https://docs.vllm.ai/)