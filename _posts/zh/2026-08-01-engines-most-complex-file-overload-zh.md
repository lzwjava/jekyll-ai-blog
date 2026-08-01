---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 引擎最复杂的文件过载
translated: true
type: note
---

没有未提交的更改，所以我无法确定你刚才在看什么。让我先概述一下我对代码库的解读，这样你可以指出具体是哪个部分。

**目前最复杂的部分是 `nanovllm/engine/model_runner.py`（263行）。** 它集成了四个独立的子系统：

| 复杂度 | 行数 | 功能说明 |
| --- | --- | --- |
| 张量并行 | ~70 | `dist.init_process_group` + `SharedMemory` RPC（`loop`/`read_shm`/`write_shm`），但默认`tensor_parallel_size=1` |
| CUDA图 | ~50 | `capture_cudagraph`、`graph_bs`、`graph.replay()`、图池——但`enforce_eager`会跳过 |
| KV缓存计算 | ~20 | 上次提交中的预算/已用/空闲×0.95 OOM 平衡逻辑 |
| 前缀缓存预填充 | ~60 | 带槽位映射、块表、`cu_seqlens_k ≠ cu_seqlens_q`分支的`prepare_prefill` |

引擎（调度器、块管理器、序列）实际上已经相当简洁。

**快速提问——你指的是"这个"？** 几个常见目标：

1. **整体`model_runner.py`** → 我会删除两个可选子系统（TP和CUDA图），因为默认配置从不会运行这大约120行的机制。
2. **KV缓存分配**（你上次的提交）→ 可以简化为约6行：`blocks = int(free_after_weights * gpu_memory_utilization / block_bytes)`。
3. **整个项目** → 这是另一个话题；`experiments`文件夹的价值在于"通过运行来学习"，所以我会保留。

你指的是哪一个？还是你在看完全不同的内容？
